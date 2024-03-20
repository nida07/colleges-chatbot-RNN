const chatButton = document.querySelector('.chatbox__button');
const chatContent = document.querySelector('.chatbox__support');

const icons = {
    isClicked: '<img src="/static/student/images/icons/ch.gif" style="width : 70px;border-radius: 50%;" />',
    isNotClicked: '<img src="/static/student/images/icons/ch.gif" style="width : 70px;border-radius: 50%;" />'
    // isClicked: 'Chat',
    // isNotClicked: 'Chat'
}
const chatbox = new InteractiveChatbox(chatButton, chatContent, icons);
chatbox.display();
chatbox.toggleIcon(false, chatButton);