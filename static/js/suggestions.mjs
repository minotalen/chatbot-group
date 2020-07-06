/**
 * Chat input suggestion implementation.
 * Authors: Kevin Katzkowski, mon janssen, Jeffrey Pillmann
 * Last modified: 06.06.2020
 */

import { sendButton } from './client.mjs';
import { closeSettings, getSettingValue } from './settings.mjs';

let suggestions = [{
      name: 'look around'
    },
    {
      name: 'pick up [item]'
    },
    {
      name: 'look at [object, item]'
    },
    {
      name: 'go to [location]'
    },
    {
      name: 'use [item in inventory]'
    } // TODO shorter option: inventory item
  ],
  userInput = document.getElementById('input-user'),
  chatForm = document.getElementById('chat-input-form'),
  visibleSuggestions,
  selectionIndex,
  currentSelection,
  arrowSelectionPriority = false,
  suggestionContainer = document.getElementById('suggestion-container'),
  hideSuggestions = false;


/**
 * Handle submit event, which is triggered by pressing enter key or send button
 */
chatForm.addEventListener('submit', (evt) => {
  // prevents default reloading on submit
  evt.preventDefault();

  findSelectedSuggestion();

  // if selection is active, insert selection text into input value
  if (selectionIndex != undefined) {
    userInput.value = filterType(visibleSuggestions[selectionIndex].innerText)[0];

    // send if suggestion type is "complete"
    if (filterType(visibleSuggestions[selectionIndex].innerText)[1] == 'complete') {
      sendButton.click();
      hideSuggestions = true;
    }

    // reset selection
    removeSuggestionSelection();
    selectionIndex = undefined;
    currentSelection = undefined;

  } else {
    sendButton.click();
    hideSuggestions = true;
  }
});


userInput.addEventListener('click', showSuggestions, false);

userInput.addEventListener('keydown', toggleSuggestions, false);

userInput.addEventListener('keyup', toggleSuggestions, false);


// TODO find a better name for this function
/**
 * Do not instantly reopen suggestion window after sending a message
 */
function toggleSuggestions() {
  if (!hideSuggestions) {
    showSuggestions();
  } else {
    hideSuggestions = false;
  }
}

/**
 * Filters out the object type (text in square brackets)
 * returns array with filtered text and object type
 */
function filterType(suggestionText) {
  let output,
    suggestionType = suggestionText.match(/\[(.*?)\]/); // filters the text between square bracket
  if (suggestionType) {
    // incomplete input, replace text field value and focus
    output = suggestionText.replace(`${suggestionType[0]}`, "");
    console.log("text:", output, "type:", suggestionType[0]);
  } else {
    // complete input, send
    output = suggestionText;
    suggestionType = "complete"; // complete means that selection will be submitted immediately
  }
  return [output, suggestionType]
}

/**
 * Shows suggestions in a window above input field.
 */
function showSuggestions() {
  visibleSuggestions = document.getElementsByClassName('suggestion');

  if (visibleSuggestions != undefined) {
    // find already selected element
    findSelectedSuggestion();
  }
  if (getSettingValue('setting-suggestions')) {

    hideSuggestions = false;

    // reset suggestions
    suggestionContainer.innerHTML = '';

    suggestions.forEach(suggestion => {
      // create suggestion div and add to container
      let div = document.createElement('div');
      div.setAttribute('class', 'suggestion');
      // div.setAttribute('tabindex', '0'); // make focusable with tab
      div.innerHTML = suggestion.name;

      // make suggestions clickable
      div.addEventListener('click', () => {
        userInput.value = filterType(suggestion.name)[0];
        // send if suggestion type is "complete"
        if (filterType(visibleSuggestions[selectionIndex].innerText)[1] == "complete") {
          sendButton.click();
          hideSuggestions = true;
        }
        userInput.focus();
      });

      // append only match suggestions
      if (userInput.value.trim() == '' || suggestion.name.includes(userInput.value)) {
        // highlight matching substring
        let sug = suggestion.name,
          val = userInput.value;
        div.innerHTML = sug.slice(0, sug.indexOf(val)) + '<mark>' + val +
          '</mark>' + sug.slice(sug.indexOf(val) + val.length, sug.length);

        suggestionContainer.appendChild(div);
      }
    });

    // display container only when it contains suggestions
    if (suggestionContainer.innerHTML != '') {
      // create suggestion heading
      let heading = document.createElement('div');
      heading.setAttribute('id', 'suggestion-heading');
      heading.innerHTML = 'SUGGESTIONS',

        // insert suggestions headline
        suggestionContainer.insertBefore(heading, suggestionContainer.firstChild);
      suggestionContainer.style.display = 'block';

      // set old selection again
      if (selectionIndex != undefined) {

        // update suggestions
        visibleSuggestions = document.getElementsByClassName('suggestion');

        // if old suggestion exist in new suggestions, calculate selectionIndex
        for (let suggestion of visibleSuggestions) {
          if (suggestion.innerText == currentSelection) {
            selectionIndex = Array.from(visibleSuggestions).indexOf(suggestion);
            break;
          } else {
            selectionIndex = undefined;
          }
        }

        // set old selection on new suggestions if old selection still exists
        if (selectionIndex != undefined) {
          visibleSuggestions[selectionIndex].classList.add('selected');
          currentSelection = visibleSuggestions[selectionIndex].innerText;
        } else {
          currentSelection = undefined;
        }
      }
    } else {
      closeSuggestions();
    }
  } else {
    selectionIndex = undefined;
  }
}


/**
 * Closes input field suggestions.
 */
function closeSuggestions() {
  suggestionContainer.style.display = 'none';

  // remove focus from textfield
  // userInput.blur();
  arrowSelectionPriority = false;
  removeSuggestionSelection();

  selectionIndex = undefined;
  currentSelection = undefined;
}


/**
 * Removes the css class '.selected' from the selected element.
 */
function removeSuggestionSelection() {
  if (visibleSuggestions != undefined) {
    // remove prior selection
    for (let suggestion of visibleSuggestions) {
      suggestion.classList.remove('selected');
    }
  }
}

/**
 * Finds the selected suggestion and sets selectionIndex and currentSelection.
 */
function findSelectedSuggestion() {
  for (let suggestion of visibleSuggestions) {
    if (suggestion.classList.contains('selected')) {
      selectionIndex = Array.from(visibleSuggestions).indexOf(suggestion);
      currentSelection = visibleSuggestions[selectionIndex].innerText;
      break;
    }
  }
}

/**
 * Suggestion selection on mouse hovering.
 */
suggestionContainer.addEventListener('mousemove', (evt) => {

  if (!arrowSelectionPriority && evt.target.classList.contains('suggestion')) {
    selectionIndex = Array.from(visibleSuggestions).indexOf(evt.target);

    removeSuggestionSelection();

    // set new selection
    visibleSuggestions[selectionIndex].classList.add('selected');
  }
});


suggestionContainer.addEventListener('mouseleave', (evt) => {
  removeSuggestionSelection();
});



window.addEventListener('mousemove', (evt) => {
  arrowSelectionPriority = false;
});


window.addEventListener('keydown', (evt) => {
  switch (evt.keyCode) {
    case 38: // arrow key up
      evt.preventDefault();
      findSelectedSuggestion();

      // calculate new selection index
      if (selectionIndex != undefined && visibleSuggestions.length == 1) {
        removeSuggestionSelection();
        selectionIndex = undefined;
      } else if (selectionIndex != undefined) {
        selectionIndex == 0 ? selectionIndex = visibleSuggestions.length - 1 : selectionIndex--;
      } else {
        selectionIndex = visibleSuggestions.length - 1;
      }

      removeSuggestionSelection();

      // set new selection
      visibleSuggestions[selectionIndex].classList.add('selected');
      currentSelection = visibleSuggestions[selectionIndex].innerText;

      arrowSelectionPriority = true;
      break;

    case 40: // arrow key down
      evt.preventDefault();
      findSelectedSuggestion();

      // calculate new selection index
      if (selectionIndex != undefined && visibleSuggestions.length == 1) {
        removeSuggestionSelection();
        selectionIndex = undefined;
      } else if (selectionIndex != undefined) {
        selectionIndex == visibleSuggestions.length - 1 ? selectionIndex = 0 : selectionIndex++;
      } else {
        selectionIndex = 0;
      }

      removeSuggestionSelection();

      // set new selection
      visibleSuggestions[selectionIndex].classList.add('selected');
      currentSelection = visibleSuggestions[selectionIndex].innerText;

      arrowSelectionPriority = true;
      break;

    case 27: // ESC key
      closeSuggestions();
      hideSuggestions = true;

      closeSettings();
      break;

    default:
      // on any key except modifier keys shift, ctrl, alt, altGr
      if (evt.keyCode != 16 && evt.keyCode != 17 && evt.keyCode != 18 && evt.keyCode != 32) userInput.focus();
      break;
  }
});


export {
  closeSuggestions,
  userInput
}
