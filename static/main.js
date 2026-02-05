async function setSource(cam_id){
  const vid = document.getElementById(`video-${cam_id}`);
  const src = document.getElementById(`src-${cam_id}`).value.trim();
  const filter = document.getElementById(`filter-${cam_id}`) ? document.getElementById(`filter-${cam_id}`).value : '';
  const strengthEl = document.getElementById(`filter-${cam_id}-strength`);
  const filter_strength = strengthEl ? parseFloat(strengthEl.value) : 1.0;
  const kernelEl = document.getElementById(`filter-${cam_id}-kernel`);
  const filter_param = kernelEl ? parseInt(kernelEl.value) : null;
  if(!src){
    alert("Nhập IP/URL camera trước khi Connect (hoặc bấm Stop để dừng).");
    return;
  }
  const res = await fetch('/set_source', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({cam_id: cam_id, source: src, filter: filter, filter_strength: filter_strength, filter_param: filter_param})
  });
  const j = await res.json();
  if(!j.ok){
    alert("Lỗi khi connect: " + (j.error||'unknown'));
    return;
  }
  // reload the img to pick new stream (add cache buster)
  vid.src = `/video_feed/${cam_id}?t=${Date.now()}&filter=${encodeURIComponent(filter)}`;
}

async function stopSource(cam_id){
  const res = await fetch('/set_source', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({cam_id: cam_id, source: '', filter: ''})
  });
  const j = await res.json();
  if(!j.ok){
    alert("Lỗi khi stop: " + (j.error||'unknown'));
    return;
  }
  const vid = document.getElementById(`video-${cam_id}`);
  setPlaceholder(vid);
}

async function capture(cam_id){
  // disable button quickly to avoid double click
  const btn = event.currentTarget;
  btn.disabled = true;
  try{
    const filter = document.getElementById(`filter-${cam_id}`) ? document.getElementById(`filter-${cam_id}`).value : '';
    const strengthEl = document.getElementById(`filter-${cam_id}-strength`);
    const filter_strength = strengthEl ? parseFloat(strengthEl.value) : 1.0;
    const kernelEl = document.getElementById(`filter-${cam_id}-kernel`);
    const filter_param = kernelEl ? parseInt(kernelEl.value) : null;
    const res = await fetch('/capture', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({cam_id: cam_id, filter: filter, filter_strength: filter_strength, filter_param: filter_param})
    });
    const j = await res.json();
    if(!j.ok){
      alert("Capture failed: " + (j.error || 'unknown'));
      return;
    }
    // set captured and processed images
    document.getElementById(`captured-${cam_id}`).src = j.image;
    document.getElementById(`fragment-${cam_id}`).src = j.processed;

    const timeBox = document.getElementById(`proc-time-${cam_id}`);
    if(timeBox && typeof j.process_time_ms === 'number'){
      timeBox.textContent = `Process time: ${j.process_time_ms.toFixed(2)} ms`;
    }
  }catch(err){
    alert("Error: " + err);
  }finally{
    btn.disabled = false;
  }
}

// Show/hide parameter controls depending on selected filter
document.addEventListener('DOMContentLoaded', () => {
  [1,2].forEach(id => {
    const sel = document.getElementById(`filter-${id}`);
    const params = document.getElementById(`filter-${id}-params`);
    const onChange = () => {
      if(!sel || !params) return;
      const v = sel.value;
      // show container when using sharpen or morphological filters
      if(v === 'sharpen' || v === 'erode' || v === 'dilate'){
        params.style.display = 'block';
      } else {
        params.style.display = 'none';
      }
      // show individual param controls
      const sdiv = params.querySelector('.sharpen-param');
      const mdiv = params.querySelector('.morph-param');
      if(sdiv) sdiv.style.display = (v === 'sharpen') ? 'block' : 'none';
      if(mdiv) mdiv.style.display = (v === 'erode' || v === 'dilate') ? 'block' : 'none';
    };
    if(sel){ sel.addEventListener('change', onChange); onChange(); }
  });
});

// --- UI helpers ---
// Static inline SVGs for gray placeholders.
const PLACEHOLDER_CAM = 'data:image/svg+xml;base64,' + btoa(
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360">`
  + `<rect width="640" height="360" fill="#d3d7dd"/>`
  + `<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"`
  + ` font-family="Arial, sans-serif" font-size="32" fill="#666">No Cam</text>`
  + `</svg>`
);

const PLACEHOLDER_IMG = 'data:image/svg+xml;base64,' + btoa(
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360">`
  + `<rect width="640" height="360" fill="#e7eaef"/>`
  + `<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"`
  + ` font-family="Arial, sans-serif" font-size="28" fill="#777">No Image</text>`
  + `</svg>`
);

function setPlaceholderCam(imgEl){
  imgEl.src = PLACEHOLDER_CAM;
}

function setPlaceholderImage(imgEl){
  imgEl.src = PLACEHOLDER_IMG;
}

// Initialize placeholders on page load so UI never collapses or shows broken images.
document.addEventListener('DOMContentLoaded', () => {
  [1,2].forEach(id => {
    const vid = document.getElementById(`video-${id}`);
    if(vid){
      setPlaceholderCam(vid);
    }
    const cap = document.getElementById(`captured-${id}`);
    if(cap){
      setPlaceholderImage(cap);
    }
    const frag = document.getElementById(`fragment-${id}`);
    if(frag){
      setPlaceholderImage(frag);
    }
  });
});
