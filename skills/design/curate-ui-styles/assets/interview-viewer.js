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
      frame.title = 'Current interview preview';
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
    setStatus('Waiting for the first preview.');
  } else if (state.mode === 'review') {
    setStatus('Review the style, then confirm in Pi if you want to save it.');
  } else if (state.answer) {
    setStatus(`Answer ${state.answer} received. Keep this tab open for the next question. ` +
        'If Pi stopped waiting, type "continue" in Pi.');
  } else if (frameReady && !submitting) {
    setStatus('The question is ready.');
  } else if (!frameReady) {
    setStatus('Opening the preview.');
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
      setStatus('Cannot reach the preview server. Retrying automatically.');
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
  setStatus('Submitting your answer.');
  try {
    const response = await fetch('/answer', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({preview: question.preview, choice}),
      signal: AbortSignal.timeout(4000),
    });
    if (response.status === 409) {
      setStatus('This question was already answered or replaced. Updating the preview.');
      return;
    }
    if (!response.ok) {
      throw new Error('Cannot submit the answer');
    }
    showState({...question, answer: choice});
  } catch {
    choices.disabled = false;
    setStatus('Could not confirm submission. Wait a moment or answer in Pi.');
  } finally {
    submitting = false;
  }
});

void poll();
