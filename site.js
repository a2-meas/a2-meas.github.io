(() => {
  'use strict';
  const HIGHLIGHT_INTERVAL_MS = 1500;
  const METHOD_COMPLETE_HOLD_MS = 10000;
  const autoStartViewport = {
    threshold: [0, 0.5],
    rootMargin: `-${getComputedStyle(document.documentElement).getPropertyValue('--header-offset').trim()} 0px -8% 0px`
  };
  const heroArt = document.querySelector('.hero-art');
  let coverVisible = true;
  function syncCoverMotion() {
    heroArt.classList.toggle('is-idle', !coverVisible || document.hidden);
  }
  new IntersectionObserver(entries => {
    coverVisible = entries[0].isIntersecting;
    syncCoverMotion();
  }, { threshold: 0 }).observe(document.querySelector('.hero'));
  document.addEventListener('visibilitychange', syncCoverMotion);
  const gallery = document.querySelector('#task-gallery');
  const announcement = document.querySelector('#gallery-announcement');
  const mediaPlayers = new Set();
  let manifest;

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function mediaURL(value) {
    if (typeof value !== 'string' || !value.trim()) throw new Error('Missing media URL');
    const url = new URL(value, document.baseURI);
    if (!['http:', 'https:', 'file:'].includes(url.protocol)) throw new Error('Unsupported media URL');
    return url.href;
  }

  function fitVideoDialog(dialog, video) {
    if (!dialog.open || !video) return;
    const ratio = video.videoWidth && video.videoHeight ? video.videoWidth / video.videoHeight : 16 / 9;
    dialog.style.setProperty('--video-aspect', String(ratio));
    const toolbarHeight = Math.ceil(dialog.querySelector('.task-dialog-toolbar').getBoundingClientRect().height);
    dialog.style.setProperty('--video-toolbar-height', `${toolbarHeight}px`);
  }
  const videoDialogObserver = new ResizeObserver(entries => {
    for (const entry of entries) {
      const dialog = entry.target.closest('.video-dialog');
      fitVideoDialog(dialog, dialog.querySelector('video'));
    }
  });
  document.querySelectorAll('.video-dialog .task-dialog-toolbar').forEach(toolbar => videoDialogObserver.observe(toolbar));
  document.querySelectorAll('.video-dialog').forEach(dialog => {
    dialog.addEventListener('loadedmetadata', event => {
      if (event.target instanceof HTMLVideoElement) fitVideoDialog(dialog, event.target);
    }, true);
  });

  const demoDialog = document.querySelector('#demo-video-dialog');
  const demoVideo = document.querySelector('#demo-modal-video');
  const demoStatus = document.querySelector('#demo-video-status');
  const demoClose = document.querySelector('#close-demo-video');
  let lastDemoTrigger = null;
  function openDemoVideo(item, trigger) {
    lastDemoTrigger = trigger;
    document.querySelector('#demo-video-title').textContent = item.title;
    demoStatus.hidden = true;
    demoVideo.src = mediaURL(item.src);
    if (item.poster) demoVideo.poster = mediaURL(item.poster);
    else demoVideo.removeAttribute('poster');
    demoVideo.setAttribute('aria-label', item.title);
    demoDialog.showModal();
    fitVideoDialog(demoDialog, demoVideo);
    demoClose.focus({ preventScroll: true });
    demoVideo.play().catch(() => {
      // Native video controls remain usable when autoplay is blocked.
      if (demoVideo.error) showDemoError();
    });
  }
  function showDemoError() {
    demoStatus.textContent = 'This video could not be loaded. Close the player and try again.';
    demoStatus.hidden = false;
  }
  demoVideo.addEventListener('error', showDemoError);
  demoClose.addEventListener('click', () => demoDialog.close());
  demoDialog.addEventListener('click', event => {
    if (event.target === demoDialog) demoDialog.close();
  });
  demoDialog.addEventListener('close', () => {
    demoVideo.pause();
    demoVideo.removeAttribute('src');
    demoVideo.load();
    demoStatus.hidden = true;
    lastDemoTrigger?.focus({ preventScroll: true });
  });
  function demoVideoEntry(item, label = item.title) {
    const button = el('button', 'text-link demo-video-entry', `${label} ↗`);
    button.type = 'button';
    button.setAttribute('aria-haspopup', 'dialog');
    button.setAttribute('aria-controls', 'demo-video-dialog');
    button.addEventListener('click', () => openDemoVideo(item, button));
    return button;
  }

  function videoCard(item, showDetails = true, headingTag = 'h3') {
    const card = el('article', 'video-card');
    const shell = el('div', 'video-shell');
    const video = document.createElement('video');
    video.preload = 'none';
    video.playsInline = true;
    video.muted = true;
    video.setAttribute('aria-label', item.title);
    video.setAttribute('aria-hidden', 'true');
    if (item.poster) video.poster = mediaURL(item.poster);
    const cover = el('button', 'video-cover');
    cover.type = 'button';
    cover.setAttribute('aria-label', `Play ${item.title}`);
    const play = el('span', 'play-icon');
    play.setAttribute('aria-hidden', 'true');
    play.innerHTML = '<svg viewBox="0 0 24 24"><path d="M6 3v18l16-9Z"/></svg>';
    cover.append(play);
    if (item.duration) cover.append(el('span', 'duration', item.duration));
    if (item.tag) cover.append(el('span', 'video-tag', item.tag));
    const error = el('p', 'video-error');
    error.hidden = true;
    error.setAttribute('role', 'status');
    const showError = () => {
      video.setAttribute('aria-hidden', 'true');
      video.controls = false;
      cover.hidden = false;
      cover.disabled = false;
      cover.setAttribute('aria-label', `Retry ${item.title}`);
      error.replaceChildren(document.createTextNode('This video could not be played. '));
      error.append(demoVideoEntry(item, 'Open video player'));
      error.hidden = false;
    };
    cover.addEventListener('click', async () => {
      error.hidden = true;
      cover.disabled = true;
      for (const player of mediaPlayers) if (player !== video) player.pause();
      try {
        if (!video.getAttribute('src')) video.src = mediaURL(item.src);
        else if (video.error) video.load();
        video.controls = true;
        video.removeAttribute('aria-hidden');
        await video.play();
        cover.hidden = true;
        cover.disabled = false;
        video.focus();
      } catch (_) {
        showError();
      }
    });
    video.addEventListener('play', () => {
      for (const player of mediaPlayers) if (player !== video) player.pause();
      cover.hidden = true;
    });
    video.addEventListener('error', showError);
    video.addEventListener('ended', () => {
      video.removeAttribute('src');
      video.load();
      video.controls = false;
      video.setAttribute('aria-hidden', 'true');
      cover.hidden = false;
      cover.disabled = false;
    });
    mediaPlayers.add(video);
    shell.append(video, cover);
    card.append(shell);
    if (showDetails) {
      card.append(el(headingTag, '', item.title));
      if (item.description) card.append(el('p', '', item.description));
    }
    card.append(error);
    return card;
  }

  const previousTask = document.querySelector('#tasks-prev');
  const nextTask = document.querySelector('#tasks-next');
  const taskMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const taskDialog = document.querySelector('#task-video-dialog');
  const modalPlayer = document.querySelector('#task-modal-player');
  const modalTitle = document.querySelector('#task-video-title');
  const modalFeedback = document.querySelector('#task-modal-feedback');
  const modalRetry = document.querySelector('#task-modal-retry');
  const modalStatus = document.querySelector('#task-modal-status');
  const taskPlayers = [];
  let openedTask = null;
  let lastTaskTrigger = null;
  let ringPhase = 0;
  let ringTarget = 0;
  let ringFrame = 0;
  let suppressTaskClick = false;
  function openTask(player, trigger) {
    if (suppressTaskClick) return;
    openedTask = player;
    lastTaskTrigger = trigger;
    modalTitle.textContent = player.item.title;
    modalStatus.hidden = true;
    modalFeedback.hidden = true;
    modalRetry.hidden = true;
    modalPlayer.replaceChildren(player.video);
    player.video.removeAttribute('aria-hidden');
    player.video.setAttribute('aria-label', player.item.title);
    player.video.controls = true;
    taskDialog.showModal();
    fitVideoDialog(taskDialog, player.video);
    player.play(true);
  }
  document.querySelector('#close-task-video').addEventListener('click', () => taskDialog.close());
  taskDialog.addEventListener('click', event => { if (event.target === taskDialog) taskDialog.close(); });
  taskDialog.addEventListener('close', () => {
    if (!openedTask) return;
    const player = openedTask;
    player.manuallyPaused = player.video.paused;
    player.video.controls = false;
    player.video.muted = true;
    player.video.setAttribute('aria-hidden', 'true');
    player.shell.insertBefore(player.video, player.expand);
    openedTask = null;
    modalStatus.hidden = true;
    modalFeedback.hidden = true;
    player.inRing = false;
    player.sync();
    lastTaskTrigger?.focus({ preventScroll: true });
  });
  modalRetry.addEventListener('click', () => {
    if (openedTask?.failed) openedTask.play(true);
  });

  function taskVideoCard(item) {
    const card = el('article', 'video-card task-tile');
    card.setAttribute('aria-label', item.title);
    const shell = el('div', 'video-shell');
    card.append(shell, el('h4', '', item.title));
    if (!item.src) {
      shell.classList.add('task-pending');
      shell.append(el('span', '', 'Video coming soon'));
      return { card, item };
    }
    const poster = document.createElement('img');
    poster.src = mediaURL(item.poster);
    poster.alt = '';
    poster.draggable = false;
    const video = document.createElement('video');
    video.preload = 'none';
    video.muted = true;
    video.defaultMuted = true;
    video.playsInline = true;
    video.loop = true;
    video.setAttribute('aria-hidden', 'true');
    video.poster = mediaURL(item.poster);
    const expand = el('button', 'task-expand');
    expand.type = 'button';
    expand.setAttribute('aria-label', `Expand ${item.title}`);
    expand.innerHTML = '<span class="task-expand-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 3H3v5M16 3h5v5M21 16v5h-5M8 21H3v-5"/></svg></span>';
    const state = el('span', 'task-preview-state');
    state.hidden = true;
    shell.append(poster, video, expand, state);
    const player = {
      card, item, shell, video, expand, front: false, visible: false,
      manuallyPaused: taskMotion.matches, failed: false, inRing: false,
      async play(explicit = false) {
        if (explicit) {
          this.manuallyPaused = false;
          if (openedTask === this) { modalStatus.hidden = true; modalFeedback.hidden = true; modalRetry.hidden = true; }
          if (this.failed) { this.failed = false; video.load(); }
        }
        if (!video.getAttribute('src')) {
          state.textContent = 'Loading…';
          state.hidden = false;
          video.src = mediaURL(item.src);
        }
        try { await video.play(); }
        catch (error) {
          if (error.name !== 'AbortError' && !this.failed) {
            state.textContent = 'Click to play';
            state.hidden = false;
            if (openedTask === this && !this.failed) {
              modalStatus.textContent = 'Use the video controls to start playback.';
              modalStatus.hidden = false;
              modalFeedback.hidden = false;
              modalRetry.hidden = true;
            }
          }
        }
        updateState();
      },
      sync() {
        if (openedTask === this) return;
        const shouldPlay = this.front && this.visible && !this.manuallyPaused && !document.hidden && !this.failed;
        if (shouldPlay && !this.inRing) this.play();
        else if (!shouldPlay && !video.paused) video.pause();
        this.inRing = shouldPlay;
      }
    };
    function updateState() {
      if (!player.failed && video.readyState >= 2) {
        state.textContent = player.manuallyPaused ? 'Paused' : '';
        state.hidden = !player.manuallyPaused;
      }
    }
    expand.addEventListener('click', () => openTask(player, expand));
    expand.addEventListener('focus', () => {
      if (!expand.matches(':focus-visible')) return;
      const bounds = card.getBoundingClientRect();
      const stage = gallery.getBoundingClientRect();
      const fullyVisible = bounds.left >= stage.left && bounds.right <= stage.right;
      if ((!player.front || !fullyVisible) && !taskDialog.open) {
        const index = taskPlayers.indexOf(player);
        const count = taskPlayers.length;
        const destination = index - (count / 4 - (gallery.clientWidth < 700 ? .02 : .5));
        ringTarget += (((destination - ringTarget) % count + count * 1.5) % count) - count / 2;
        animateRing();
      }
    });
    video.addEventListener('play', () => { state.hidden = true; updateState(); });
    video.addEventListener('pause', updateState);
    video.addEventListener('loadeddata', updateState);
    video.addEventListener('error', () => {
      player.failed = true;
      player.inRing = false;
      state.textContent = 'Click to retry';
      state.hidden = false;
      if (openedTask === player) {
        const link = el('a', '', 'Open video directly ↗');
        link.href = mediaURL(item.src);
        link.target = '_blank'; link.rel = 'noopener';
        modalStatus.replaceChildren(document.createTextNode('Video unavailable. '), link);
        modalStatus.hidden = false;
        modalFeedback.hidden = false;
        modalRetry.hidden = false;
      }
    });
    const observer = new IntersectionObserver(entries => {
      player.visible = entries[0].isIntersecting;
      player.sync();
    });
    observer.observe(shell);
    return player;
  }

  function layoutRing() {
    const width = gallery.clientWidth;
    const mobile = width < 700;
    const cardWidth = mobile ? 194 : Math.min(212, Math.max(156, width * .15));
    const radiusX = (Math.max(width, mobile ? 1020 : width) - cardWidth * .76) / 2;
    const radiusY = mobile ? 112 : 142;
    const centerY = mobile ? 204 : 248;
    gallery.style.setProperty('--orbit-radius-x', `${radiusX}px`);
    gallery.style.setProperty('--orbit-radius-y', `${radiusY}px`);
    gallery.style.setProperty('--orbit-center-y', `${centerY}px`);
    gallery.style.setProperty('--orbit-card-width', `${cardWidth}px`);
    const count = taskPlayers.length;
    taskPlayers.forEach((player, index) => {
      const angle = ((index - ringPhase + (mobile ? .02 : .5)) / count) * Math.PI * 2;
      const depth = Math.sin(angle);
      const front = ((angle % (Math.PI * 2) + Math.PI * 2) % (Math.PI * 2)) < Math.PI;
      const centerEmphasis = Math.exp(-Math.pow(Math.cos(angle) / .38, 2));
      const scale = front ? .66 + .22 * depth + .52 * centerEmphasis : .66 + .14 * depth;
      const x = width / 2 - radiusX * Math.cos(angle);
      const y = centerY + radiusY * depth;
      player.card.style.transform = `translate3d(${x}px,${y}px,0) translate(-50%,-50%) scale(${scale})`;
      player.card.style.zIndex = String(Math.round((depth + 1) * 100));
      player.card.style.opacity = String(front ? 1 : .30 + .22 * (depth + 1));
      player.card.style.filter = front ? 'none' : `blur(${1.8 - depth * .8}px)`;
      player.card.classList.toggle('is-rear', !front);
      player.front = front;
      if (player.video) player.sync();
    });
  }
  function animateRing() {
    if (ringFrame) return;
    const tick = () => {
      const delta = ringTarget - ringPhase;
      ringPhase = taskMotion.matches || Math.abs(delta) < .001 ? ringTarget : ringPhase + delta * .17;
      layoutRing();
      if (ringPhase !== ringTarget) ringFrame = requestAnimationFrame(tick);
      else ringFrame = 0;
    };
    ringFrame = requestAnimationFrame(tick);
  }
  function rotateRing(amount) { ringTarget += amount; animateRing(); }
  previousTask.addEventListener('click', () => rotateRing(-1));
  nextTask.addEventListener('click', () => rotateRing(1));
  new ResizeObserver(layoutRing).observe(gallery);
  gallery.addEventListener('keydown', event => {
    if (event.target !== gallery) return;
    if (['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) {
      event.preventDefault();
      if (event.key === 'Home') { ringTarget = 0; animateRing(); }
      else if (event.key === 'End') { ringTarget = taskPlayers.length / 2; animateRing(); }
      else rotateRing(event.key === 'ArrowRight' ? 1 : -1);
    }
  });
  gallery.addEventListener('wheel', event => {
    const horizontal = Math.abs(event.deltaX) > Math.abs(event.deltaY) * .5;
    if (!horizontal && !event.shiftKey) return;
    event.preventDefault();
    const delta = horizontal ? event.deltaX : event.deltaY;
    rotateRing(delta * (event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? 400 : 1) / 150);
  }, { passive: false });
  let drag = null;
  gallery.addEventListener('pointerdown', event => {
    if (event.button !== 0) return;
    drag = { id: event.pointerId, x: event.clientX, y: event.clientY, lastX: event.clientX, moved: false };
  });
  gallery.addEventListener('pointermove', event => {
    if (!drag || drag.id !== event.pointerId) return;
    const dx = event.clientX - drag.x;
    const dy = event.clientY - drag.y;
    if (!drag.moved && Math.abs(dx) > 7 && Math.abs(dx) > Math.abs(dy)) {
      drag.moved = true;
      gallery.setPointerCapture(event.pointerId);
      gallery.classList.add('is-dragging');
    }
    if (drag.moved) {
      event.preventDefault();
      rotateRing((drag.lastX - event.clientX) / 150);
      drag.lastX = event.clientX;
    }
  });
  const stopDrag = event => {
    if (!drag || drag.id !== event.pointerId) return;
    suppressTaskClick = drag.moved;
    if (gallery.hasPointerCapture(event.pointerId)) gallery.releasePointerCapture(event.pointerId);
    gallery.classList.remove('is-dragging');
    drag = null;
    if (suppressTaskClick) setTimeout(() => { suppressTaskClick = false; }, 0);
  };
  gallery.addEventListener('pointerup', stopDrag);
  gallery.addEventListener('pointercancel', stopDrag);
  taskMotion.addEventListener('change', event => {
    taskPlayers.forEach(player => {
      if (player.video) { player.manuallyPaused = event.matches; player.inRing = false; player.sync(); }
    });
  });
  document.addEventListener('visibilitychange', () => taskPlayers.forEach(player => { if (player.video) player.sync(); }));

  function renderGallery() {
    gallery.replaceChildren();
    if (!manifest.tasks.length) gallery.append(el('p', 'loading-note', 'Task demonstrations coming soon.'));
    for (const task of manifest.tasks) {
      const player = taskVideoCard(task);
      taskPlayers.push(player);
      gallery.append(player.card);
    }
    const ready = manifest.tasks.some(task => task.src);
    announcement.textContent = ready ? 'Task videos loaded.' : 'Task demonstrations coming soon.';
    gallery.setAttribute('aria-busy', 'false');
    previousTask.disabled = nextTask.disabled = manifest.tasks.length < 2;
    layoutRing();
  }

  async function initMedia() {
    try {
      const response = await fetch('data/videos.json');
      if (!response.ok) throw new Error('Video manifest unavailable');
      manifest = await response.json();
      for (const correction of manifest.corrections) document.querySelector('#correction-videos').append(videoCard(correction, true, 'h5'));
      document.querySelector('#coffee-video').append(videoCard(manifest.coffee, false));
      renderGallery();
    } catch (_) {
      gallery.setAttribute('aria-busy', 'false');
      gallery.replaceChildren(el('p', 'loading-note', 'The media gallery could not be loaded. Reload the page to try again.'));
      for (const [selector, src, text] of [
        ['#correction-videos', 'assets/videos/correction-step-2.mp4', 'Open Step 2 recovery'],
        ['#correction-videos', 'assets/videos/correction-step-7.mp4', 'Open Step 7 recovery'],
        ['#coffee-video', 'assets/videos/coffee.mp4', 'Open the full coffee sequence']
      ]) {
        document.querySelector(selector).append(demoVideoEntry({ src, title: text }, text));
      }
    }
  }

  const principles = document.querySelector('.principles');
  const principleCards = [...principles.querySelectorAll('.principle-card')];
  const principleHover = matchMedia('(hover: hover)');
  let principleTimer = null;
  let principlePointerCard = null;
  let principlesVisible = false;
  let principlesStarted = false;
  principles.dataset.autoStarted = 'false';
  function activatePrinciple(activeCard) {
    principleCards.forEach(card => {
      const active = card === activeCard;
      card.classList.toggle('is-active', active);
      card.setAttribute('aria-pressed', String(active));
    });
  }
  function syncPrincipleCycle() {
    clearTimeout(principleTimer);
    principleTimer = null;
    const focusedCard = principles.contains(document.activeElement) && document.activeElement.matches(':focus-visible') ? document.activeElement.closest('.principle-card') : null;
    const pointerCard = principlePointerCard || (principleHover.matches && principleCards.find(card => card.matches(':hover')));
    const selected = pointerCard || focusedCard;
    principles.dataset.flowMode = selected ? 'manual' : 'auto';
    if (selected) { activatePrinciple(selected); return; }
    if (!principlesVisible || !principlesStarted || document.hidden || taskMotion.matches) return;
    principleTimer = setTimeout(() => {
      const current = principleCards.findIndex(card => card.classList.contains('is-active'));
      activatePrinciple(principleCards[(current + 1) % principleCards.length]);
      syncPrincipleCycle();
    }, HIGHLIGHT_INTERVAL_MS);
  }
  principleCards.forEach(card => {
    card.addEventListener('pointerenter', event => {
      if (event.pointerType !== 'touch') {
        principlePointerCard = card;
        syncPrincipleCycle();
      }
    });
    card.addEventListener('pointerleave', event => {
      if (event.pointerType !== 'touch' && principlePointerCard === card) { principlePointerCard = null; queueMicrotask(syncPrincipleCycle); }
    });
    card.addEventListener('focus', () => { activatePrinciple(card); syncPrincipleCycle(); });
    card.addEventListener('click', () => { activatePrinciple(card); syncPrincipleCycle(); });
  });
  principles.addEventListener('pointermove', event => {
    if (event.pointerType === 'touch') return;
    const card = event.target.closest('.principle-card');
    if (principlePointerCard !== card) { principlePointerCard = card; syncPrincipleCycle(); }
  });
  principles.addEventListener('pointerleave', event => {
    if (event.pointerType !== 'touch') {
      principlePointerCard = null;
      syncPrincipleCycle();
    }
  });
  principles.addEventListener('focusout', () => queueMicrotask(syncPrincipleCycle));
  new IntersectionObserver(entries => {
    principlesVisible = entries[0].isIntersecting;
    if (!principlesVisible) {
      principlesStarted = false;
      principles.dataset.autoStarted = 'false';
      if (principles.dataset.flowMode !== 'manual') activatePrinciple(principleCards[0]);
    }
    syncPrincipleCycle();
  }, { threshold: 0 }).observe(principles);
  new IntersectionObserver(entries => {
    if (entries[0].isIntersecting && entries[0].intersectionRatio >= 0.5 && !principlesStarted) {
      principlesStarted = true;
      principles.dataset.autoStarted = 'true';
      activatePrinciple(principleCards[0]);
      syncPrincipleCycle();
    }
  }, autoStartViewport).observe(principleCards[0]);
  document.addEventListener('visibilitychange', syncPrincipleCycle);
  taskMotion.addEventListener('change', syncPrincipleCycle);

  document.querySelectorAll('.mobile-nav a').forEach(link => {
    link.addEventListener('click', () => document.querySelector('.mobile-nav').removeAttribute('open'));
  });

  const resultJumps = document.querySelectorAll('.results-jumps a');
  const updateResultJump = () => resultJumps.forEach(link => {
    if (link.hash === window.location.hash) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
  window.addEventListener('hashchange', updateResultJump);
  updateResultJump();

  // Independently cycle the paper's Method subpanels; keep all other media untouched.
  document.querySelectorAll('[data-method-flow]').forEach(flow => {
    const modules = [...flow.querySelectorAll('[data-flow-module]')];
    const stages = [...new Set(modules.map(module => module.dataset.flowStage || module.dataset.flowModule))];
    const motion = matchMedia('(prefers-reduced-motion: reduce)');
    const hoverCapable = matchMedia('(hover: hover)');
    let current = 0, timer, visible = false, started = false, hoveredModule = null;
    flow.dataset.autoStarted = 'false';
    function activate(index) {
      current = index;
      const complete = index === stages.length;
      flow.dataset.flowState = complete ? 'complete' : stages[index];
      modules.forEach((module, i) => {
        const active = complete || (module.dataset.flowStage || module.dataset.flowModule) === stages[index];
        module.classList.toggle('is-active', active);
        module.setAttribute('aria-pressed', String(active));
      });
    }
    function selectManual(module) {
      current = stages.indexOf(module.dataset.flowStage || module.dataset.flowModule);
      flow.dataset.flowState = stages[current];
      flow.dataset.flowMode = 'manual';
      flow.dataset.manualModule = module.dataset.flowModule;
      modules.forEach(item => {
        item.classList.toggle('is-active', item === module);
        item.setAttribute('aria-pressed', String(item === module));
      });
    }
    function sync() {
      clearTimeout(timer);
      const pointer = hoveredModule || (hoverCapable.matches && modules.find(module => module.matches(':hover')));
      const focused = flow.contains(document.activeElement) && document.activeElement.matches(':focus-visible') ? document.activeElement.closest('[data-flow-module]') : null;
      const selected = pointer || focused;
      if (selected) {
        selectManual(selected);
        return;
      }
      if (flow.dataset.flowMode === 'manual') activate(current);
      flow.dataset.flowMode = 'auto';
      delete flow.dataset.manualModule;
      if (!visible || !started || document.hidden || motion.matches || document.querySelector('dialog[open]')) return;
      timer = setTimeout(() => { activate((current + 1) % (stages.length + 1)); sync(); }, current === stages.length ? METHOD_COMPLETE_HOLD_MS : HIGHLIGHT_INTERVAL_MS);
    }
    activate(0);
    modules.forEach((module, index) => {
      const stageIndex = stages.indexOf(module.dataset.flowStage || module.dataset.flowModule);
      module.addEventListener('pointerenter', event => {
        if (event.pointerType !== 'touch') { hoveredModule = module; sync(); }
      });
      module.addEventListener('pointerleave', event => {
        if (event.pointerType !== 'touch' && hoveredModule === module) { hoveredModule = null; queueMicrotask(sync); }
      });
      module.addEventListener('focus', () => {
        if (module.matches(':focus-visible')) sync();
      });
      module.addEventListener('click', () => { selectManual(module); clearTimeout(timer); });
      module.addEventListener('keydown', event => {
        if (!['ArrowRight','ArrowLeft','ArrowDown','ArrowUp','Home','End'].includes(event.key)) return;
        event.preventDefault();
        const next = event.key === 'Home' ? 0 : event.key === 'End' ? stages.length-1 : (stageIndex + (['ArrowRight','ArrowDown'].includes(event.key) ? 1 : -1) + stages.length) % stages.length;
        activate(next); modules.find(item => (item.dataset.flowStage || item.dataset.flowModule) === stages[next]).focus(); sync();
      });
    });
    flow.addEventListener('pointermove', event => {
      if (event.pointerType === 'touch') return;
      const module = event.target.closest('[data-flow-module]');
      if (hoveredModule !== module) { hoveredModule = module; sync(); }
    });
    flow.addEventListener('pointerleave', () => { hoveredModule = null; sync(); });
    flow.addEventListener('focusout', () => queueMicrotask(sync));
    new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      if (!visible) {
        started = false;
        flow.dataset.autoStarted = 'false';
        if (flow.dataset.flowMode !== 'manual') activate(0);
      }
      sync();
    }, {threshold: 0}).observe(flow);
    new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && entries[0].intersectionRatio >= 0.5 && !started) {
        started = true;
        flow.dataset.autoStarted = 'true';
        activate(0);
        sync();
      }
    }, autoStartViewport).observe(modules[0]);
    document.addEventListener('visibilitychange', sync);
    document.querySelector('#figure-dialog').addEventListener('close', sync);
    motion.addEventListener('change', sync);
  });

  const dialog = document.querySelector('#figure-dialog');
  const expandedFigure = document.querySelector('#expanded-figure');
  let lastFigureTrigger;
  document.querySelectorAll('[data-figure]').forEach(button => {
    button.addEventListener('click', () => {
      lastFigureTrigger = button;
      expandedFigure.src = button.dataset.figure;
      expandedFigure.alt = button.querySelector('img').alt;
      document.querySelector('#figure-caption').textContent = button.dataset.caption;
      const caption = button.closest('figure').querySelector('.figure-description');
      const expandedDescription = document.querySelector('#expanded-figure-description');
      expandedDescription.replaceChildren(...(caption ? Array.from(caption.querySelectorAll('.figure-brief'), node => node.cloneNode(true)) : []));
      expandedDescription.hidden = expandedDescription.childElementCount === 0;
      dialog.showModal();
    });
  });
  document.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => lastFigureTrigger?.focus());

  const emailCopyButton = document.querySelector('#copy-email');
  const emailStatus = document.querySelector('#email-copy-status');
  let emailFeedbackTimer;
  emailCopyButton.addEventListener('click', async () => {
    const email = 'zhipengzhang@sjtu.edu.cn';
    clearTimeout(emailFeedbackTimer);
    emailCopyButton.disabled = true;
    emailStatus.hidden = true;
    emailStatus.classList.remove('email-feedback-error');
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard API unavailable');
      await navigator.clipboard.writeText(email);
      emailStatus.textContent = 'Email copied';
      emailStatus.hidden = false;
      emailFeedbackTimer = setTimeout(() => { emailStatus.hidden = true; }, 1800);
    } catch (_) {
      const address = el('span', 'email-address', email);
      address.tabIndex = -1;
      emailStatus.replaceChildren(document.createTextNode('Select and copy: '), address);
      emailStatus.classList.add('email-feedback-error');
      emailStatus.hidden = false;
      address.focus();
      const range = document.createRange();
      range.selectNodeContents(address);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
    } finally {
      emailCopyButton.disabled = false;
    }
  });

  document.querySelector('#copy-citation').addEventListener('click', async () => {
    const citation = document.querySelector('#bibtex');
    const status = document.querySelector('#copy-status');
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard API unavailable');
      await navigator.clipboard.writeText(citation.textContent);
      status.textContent = 'Citation copied.';
    } catch (_) {
      const range = document.createRange();
      range.selectNodeContents(citation);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = 'Citation selected. Press Ctrl+C or ⌘C to copy.';
    }
  });

  initMedia();
})();
