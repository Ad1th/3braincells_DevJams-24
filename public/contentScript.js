import { currentTab } from "./public/background.js";

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log("the message sent: ", request)
  if (sender.tab) {
    // Message came from a content script running in a tab
    console.log(`Message from content script on tab: ${sender.tab.id}, URL: ${sender.url}`);
} else if (sender.id === chrome.runtime.id) {
    // Message came from within the extension itself (e.g., popup or background)
    console.log('Message from the extension (popup or background script).');
} else {
    console.log('Unknown sender.');
}
    if (request.action === "getPageContent") {
      sendResponse({content: document.body.innerText});
    }
  });


// function currentTab(){
//   chrome.tabs.query({active: "true", currentWindow: "true"}, (tabs) => {
//     const currentTabId = tabs[0].id;
//     console.log("current tab", currentTabId);
//   } )
//   return currentTabId;
// }


// function scrapePageContent() {
//   const textContent = currentTab()
//   const wordCount = textContent.split(/\s+/).length; // count the number of words


// }

function scrapePageContent(){
  
}