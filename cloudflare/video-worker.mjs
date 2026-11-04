// Pages static assets currently ignore Range. Only the private Pages package
// installs this adapter; the ordinary static/GitHub Pages package stays unchanged.
// Filled from the final hosting copies, including any resized videos.
const VIDEO_BYTES = /* @video-sizes */ {};

export function parseRange(value, size) {
  const match = /^bytes=(\d*)-(\d*)$/.exec(value.trim());
  // Ignore unsupported units and multipart syntax, as permitted by HTTP.
  if (!match) return null;
  const [, left, right] = match;
  if ((!left && !right) || size === 0) return false;
  const first = Number(left || right);
  const last = right && left ? Number(right) : size - 1;
  if (!Number.isSafeInteger(first) || !Number.isSafeInteger(last)) return false;
  if (!left) return first > 0 ? [Math.max(0, size - first), size - 1] : false;
  if (first >= size || first > last) return false;
  return [first, Math.min(last, size - 1)];
}

function matchesIfRange(value, headers) {
  if (!value) return true;
  if (value.startsWith('"')) return value === headers.get('ETag');
  if (value.startsWith('W/')) return false;
  const modified = Date.parse(headers.get('Last-Modified') || '');
  const requested = Date.parse(value);
  return Number.isFinite(modified) && Number.isFinite(requested) && modified <= requested;
}

function privateHeaders(headers) {
  const output = new Headers(headers);
  output.set('Accept-Ranges', 'bytes');
  output.set('Cache-Control', 'private, no-store');
  return output;
}

async function storeFullVideo(cache, key, body, size, headers) {
  const cacheHeaders = new Headers(headers);
  cacheHeaders.set('Cache-Control', 'public, max-age=86400');
  cacheHeaders.delete('Set-Cookie');
  const stream = new FixedLengthStream(size);
  // Native pipe avoids processing the full video chunk-by-chunk in JavaScript.
  await Promise.all([
    body.pipeTo(stream.writable),
    cache.put(key, new Response(stream.readable, { headers: cacheHeaders }))
  ]);
}

function prefixStream(body, length) {
  const reader = body.getReader();
  let remaining = length;
  return new ReadableStream({
    async pull(controller) {
      const { done, value } = await reader.read();
      if (done) { controller.close(); return; }
      const count = Math.min(value.byteLength, remaining);
      controller.enqueue(value.subarray(0, count));
      remaining -= count;
      if (!remaining) { controller.close(); await reader.cancel(); }
    },
    cancel(reason) { return reader.cancel(reason); }
  });
}

export default {
  async fetch(request, env, context) {
    const path = new URL(request.url).pathname;
    // Range applies to GET; let the static binding handle HEAD and other methods.
    if (!/^\/assets\/videos\/[^/]+\.mp4$/i.test(path) || request.method !== 'GET') {
      return env.ASSETS.fetch(request);
    }
    // ASSETS is the internal static binding, not a public origin. Access still
    // authenticates every external request before this worker is invoked.
    const asset = await env.ASSETS.fetch(new Request(request.url, {
      headers: { 'Accept-Encoding': 'identity' }
    }));
    if (asset.status !== 200) return asset;
    const size = asset.headers.has('Content-Length')
      ? Number(asset.headers.get('Content-Length')) : VIDEO_BYTES[path];
    if (!Number.isSafeInteger(size) || size < 0 || asset.headers.has('Content-Encoding')) {
      return asset;
    }
    const headers = new Headers(asset.headers);
    headers.set('Accept-Ranges', 'bytes');
    const requested = request.headers.get('Range');
    const range = requested && matchesIfRange(request.headers.get('If-Range'), headers)
      ? parseRange(requested, size) : null;
    if (range === false) {
      context.waitUntil(asset.body.cancel());
      headers.set('Content-Range', `bytes */${size}`);
      headers.set('Content-Length', '0');
      return new Response(null, { status: 416, headers });
    }
    // Let Cloudflare's native cache slice ranges. Passing a large file through
    // JavaScript chunk-by-chunk can exceed the Free plan's CPU budget.
    // The cache is internal to this protected app; client responses stay private.
    const key = new URL(request.url);
    key.search = '';
    key.searchParams.set('__video_etag', headers.get('ETag') || String(size));
    const cache = caches.default;
    const cacheKey = new Request(key);
    let cached = await cache.match(cacheKey);
    if (!cached) {
      // Initial playback must not wait for the complete file to enter cache.
      // Stream open-ended playback, or the small initial metadata probe, now;
      // fill the native range cache in parallel for subsequent seeks.
      if (!range || (range[0] === 0 && (range[1] === size - 1 || range[1] < 65536))) {
        const [clientBody, cacheBody] = asset.body.tee();
        context.waitUntil(storeFullVideo(cache, cacheKey, cacheBody, size, headers).catch(() => {}));
        const outputHeaders = privateHeaders(headers);
        if (range) {
          const length = range[1] + 1;
          outputHeaders.set('Content-Range', `bytes 0-${range[1]}/${size}`);
          outputHeaders.set('Content-Length', String(length));
          return new Response(length === size ? clientBody : prefixStream(clientBody, length), { status: 206, headers: outputHeaders });
        }
        return new Response(clientBody, { status: 200, headers: outputHeaders });
      }
      await storeFullVideo(cache, cacheKey, asset.body, size, headers);
    } else {
      context.waitUntil(asset.body.cancel());
      context.waitUntil(cached.body.cancel());
    }
    const lookupHeaders = range ? { Range: `bytes=${range[0]}-${range[1]}` } : {};
    cached = await cache.match(new Request(key, { headers: lookupHeaders }));
    if (!cached) return new Response('Video temporarily unavailable', { status: 503, headers: { 'Retry-After': '1' } });
    const outputHeaders = privateHeaders(cached.headers);
    return new Response(cached.body, { status: cached.status, headers: outputHeaders });
  }
};
