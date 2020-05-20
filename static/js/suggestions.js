/**
 * Chat input suggestion implementation.
 * Authors: Kevin Katzkowski, mon janssen, Jeffrey Pillmann
 * Last modfidied: 19.05.2020
 */

import { sendButton } from './client.js';

let suggestions = [
  {name: 'suggestion'}, 
  {name: 'alpha suggestion'},
  {name: 'suggestion test'},
  {name: 'look around'},
  {name: 'pick up [object]'},
  {name: 'open [object]'},
  {name: 'use [object]'},
  {name: 'inspect [object]'},
  {name: 'give [object] '}, // two layers
  {name: 'give [object] to [person]'},
  {name: 'go to [location]'},
  {name: 'talk to [person]'},
  {name: 'about [any]'},
  {name: 'look at [person, object]'}],
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
  if(selectionIndex != undefined) {
    userInput.value = visibleSuggestions[selectionIndex].innerText + ' ';

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
 

/**
 * Do not instantly reopen suggestion window after sending a message
 */
function toggleSuggestions() {
  if(!hideSuggestions) {
    showSuggestions();
  } else {
    hideSuggestions = false;
  }
}


/**
 * Shows suggestions in a window above input field.
 */
function showSuggestions() {
  hideSuggestions = false;
  visibleSuggestions = document.getElementsByClassName('suggestion');

  if(visibleSuggestions != undefined) {
    // find already selected element 
    findSelectedSuggestion();
  }
  
  // reset suggestions
  suggestionContainer.innerHTML = '';

  suggestions.forEach(suggestion => {
    // create suggestion div and add to container
    let div = document.createElement('div');
    div.setAttribute('class', 'suggestion');
    div.setAttribute('tabindex', '0'); // make focusable
    div.innerHTML = suggestion.name;

    // make suggestions clickable
    div.addEventListener('click', () => {
      userInput.value = suggestion.name;
      userInput.focus();
    });
    
    // append only match suggestions
    if(userInput.value.trim() == '' || suggestion.name.includes(userInput.value)) {
      // highlight matching substring
      let sug = suggestion.name, val = userInput.value;
      div.innerHTML = sug.slice(0, sug.indexOf(val)) + '<mark>' + val 
        + '</mark>' + sug.slice(sug.indexOf(val) + val.length, sug.length); 

      suggestionContainer.appendChild(div);
    }
  });
  
  // display container only when it contains suggestions
  if(suggestionContainer.innerHTML != '') {
    // create suggestion heading
    let heading = document.createElement('div');
    heading.setAttribute('id', 'suggestion-heading');
    heading.innerHTML = 'SUGGESTIONS',

    // insert suggestions headline
    suggestionContainer.insertBefore(heading, suggestionContainer.firstChild);
    suggestionContainer.style.display = 'block';

    // set old selection again
    if(selectionIndex != undefined) {

      // update suggestions 
      visibleSuggestions = document.getElementsByClassName('suggestion');
    
      // if old suggestion exist in new suggestions, calculate selectionIndex
      for (let suggestion of visibleSuggestions) {
        if(suggestion.innerText == currentSelection) { 
          selectionIndex = Array.from(visibleSuggestions).indexOf(suggestion);
          break;
        } else {
          selectionIndex = undefined;
        }
      }
      
      // set old selection on new suggestions if old selection still exists
      if(selectionIndex != undefined) {
        visibleSuggestions[selectionIndex].classList.add('selected');
        currentSelection =  visibleSuggestions[selectionIndex].innerText;
      } else {
        currentSelection = undefined;
      }
    }
  } else {
    closeSuggestions();
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
  if(visibleSuggestions != undefined) {
    // remove prior selection
    for(let suggestion of visibleSuggestions) {
      suggestion.classList.remove('selected');
    }
  }
}

/**
 * Finds the selected suggestion and sets selectionIndex and currentSelection.
 */
function findSelectedSuggestion() {
  for (let suggestion of visibleSuggestions) {
    if(suggestion.classList.contains('selected')) {
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

  if(!arrowSelectionPriority && evt.target.classList.contains('suggestion')) {
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
      if(selectionIndex != undefined && visibleSuggestions.length == 1) {
        removeSuggestionSelection();
        selectionIndex = undefined;
      } else if(selectionIndex != undefined) {
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
      if(selectionIndex != undefined && visibleSuggestions.length == 1) {
        removeSuggestionSelection();
        selectionIndex = undefined;
      } else if(selectionIndex != undefined) {
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
    
    default:
      break;
  }
});


export { closeSuggestions, userInput }
