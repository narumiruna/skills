'use strict';

const form = document.querySelector('#answer');
const choices = form.querySelector('fieldset');
const preview = document.querySelector('#preview');
const status = document.querySelector('#status');

let current = null;
let frameReady = false;
let submitting = false;
let pollTimer;
let polling = false;
let submissionVersion = 0;

function setStatus(message) {
  if (status.textContent !== message) {
    status.textContent = message;
  }
}

function showState(state) {
  if (state?.preview !== current?.preview) {
    frameReady = false;
    form.reset();
    if (state) {
      const frame = document.createElement('iframe');
      frame.title = '目前題目的視覺預覽';
      frame.setAttribute('sandbox', '');
      frame.addEventListener('load', () => {
        frameReady = true;
        showState(current);
      }, {once: true});
      frame.src = '/' + state.preview;
      preview.replaceChildren(frame);
    } else {
      preview.replaceChildren();
    }
  }

  current = state;
  form.hidden = state?.mode !== 'question';
  choices.disabled = !frameReady || submitting || Boolean(state?.answer);

  if (!state) {
    setStatus('等待第一個預覽。');
  } else if (state.mode === 'review') {
    setStatus('請查看整理後的風格，並在 Pi 確認是否儲存。');
  } else if (state.answer) {
    setStatus(`已收到 ${state.answer}，請在此等候下一題。如 Pi 已停止等待，請在 Pi 輸入「繼續」。`);
  } else if (frameReady && !submitting) {
    setStatus('新題目已就緒。');
  } else if (!frameReady) {
    setStatus('正在開啟預覽。');
  }
}

async function poll() {
  if (polling || document.hidden) {
    return;
  }
  polling = true;
  try {
    if (!submitting) {
      const version = submissionVersion;
      const response = await fetch('/state', {signal: AbortSignal.timeout(4000)});
      if (!response.ok) {
        throw new Error('Cannot read the current question');
      }
      const state = await response.json();
      if (version === submissionVersion) {
        showState(state);
      }
    }
  } catch {
    if (!submitting) {
      choices.disabled = true;
      setStatus('暫時無法連到 Pi 的預覽服務，會自動重試。');
    }
  } finally {
    polling = false;
    if (!document.hidden) {
      pollTimer = setTimeout(poll, 1000);
    }
  }
}

document.addEventListener('visibilitychange', () => {
  clearTimeout(pollTimer);
  void poll();
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (choices.disabled || current?.mode !== 'question') {
    return;
  }
  const choice = new FormData(form).get('choice');
  const question = current;
  submitting = true;
  submissionVersion += 1;
  choices.disabled = true;
  setStatus('正在送出答案。');
  try {
    const response = await fetch('/answer', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({preview: question.preview, choice}),
      signal: AbortSignal.timeout(4000),
    });
    if (response.status === 409) {
      setStatus('這題已回答或已換題，正在更新頁面。');
      return;
    }
    if (!response.ok) {
      throw new Error('Cannot submit the answer');
    }
    showState({...question, answer: choice});
  } catch {
    choices.disabled = false;
    setStatus('未能確認是否送出。請稍候，或回到 Pi 回答。');
  } finally {
    submitting = false;
  }
});

void poll();
