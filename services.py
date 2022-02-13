from bs4 import BeautifulSoup
import datetime
from models import Message, MessageGroup, Divider
from utilities import GetDateTime

PROCESS_FILTER_CLASSES = ['message-group']

def ProcessMessageBoard(messageBoardHTML):
    messagegroups = []
    parsedhtml = BeautifulSoup(messageBoardHTML,'html.parser')
    ndivs = parsedhtml.find_all(name='div', recursive=False)

    processlist = []
    # Iterate through the divs one by one
    for div in ndivs:
        classnames = div.attrs["class"]

        for filter in PROCESS_FILTER_CLASSES:
            if filter in classnames:
                # Remove other class names
                # TODO : Review decision to remove existing class names
                div.attrs["class"] = [filter]
                processlist.append(div)
                break

    for div in processlist:
        if 'message-group' in div.attrs["class"]:
            messagegroups.append(ProcessMessageGroup(div))
    # Process each div based on class name.

    return messagegroups


def ProcessMessageGroup(bsMessageGroupElement:BeautifulSoup):
    # Processess and returns a list of Messages
    # [<Message>, <Message>]

    username = bsMessageGroupElement.select(".comment .message.first .user-name")[0].text.strip()
    timestamp = bsMessageGroupElement.select(".comment .message.first .timestamp")[0].text.strip()
    messagecontent = bsMessageGroupElement.select(".comment .message .message-text .markup")

    messages = [m.text.strip() for m in messagecontent]

    # TODO : Convert the time text to an actual date time value for storage.
    # TODO Update the date time stamp with message group DT Stamp
    ts = GetDateTime(timestamp)
    mg = MessageGroup(ts)
    mg.username = username

    for m in messages:
        #print('-------')
        #print(m)
        mo = Message(m)
        mo.SetCreatedDate(ts)
        mg.AppendMessage(mo)

    return mg




if __name__ == "__main__":
    sampleHTMLContent = """
    
<div class="welcome-message">
 <h1 class="old-h1">
  Welcome to your server, captain_arroganto!
 </h1>
 <div class="item-container">
  <div class="icon exclamation">
  </div>
  <p>
   <strong>
    Learn about Discord
   </strong>
   at your own pace by exploring the floating quest indicators.
  </p>
 </div>
 <div class="item-container">
  <div class="icon share">
  </div>
  <p>
   <strong>
    Invite your friends
   </strong>
   to this server by clicking on a
   <a rel="noreferrer">
    share button
   </a>
   when you're ready.
  </p>
 </div>
 <div class="item-container">
  <div class="icon apps">
  </div>
  <p>
   <strong>
    Download
   </strong>
   the
   <a rel="noreferrer">
    desktop app
   </a>
   for system-wide Push to Talk, lower CPU and bandwidth usage, and more.
  </p>
 </div>
 <div class="item-container">
  <div class="icon mobile">
  </div>
  <p>
   <strong>
    Stay connected
   </strong>
   to your server from
   <a rel="noreferrer">
    your smartphone
   </a>
   and even use Discord while console gaming.
  </p>
 </div>
 <div class="item-container">
  <div class="icon twitter">
  </div>
  <p>
   <strong>
    Reach us
   </strong>
   via
   <a href="https://support.discordapp.com/hc/en-us" rel="noreferrer" target="_blank">
    our help desk
   </a>
   or on Twitter
   <a href="http://www.twitter.com/discordapp" rel="noreferrer" target="_blank">
    @discordapp
   </a>
   if you have any
questions or need help.
  </p>
 </div>
 <div class="empty-message">
 </div>
</div>
<div class="message-group has-divider hide-overflow">
 <div class="avatar-large stop-animation" style='background-image: url("/assets/0e291f67c9274a1abdddeb3fd919cbaa.png");'>
 </div>
 <div class="comment">
  <div class="message first">
   <div class="body">
    <h2 class="old-h2">
     <span class="username-wrapper">
      <strong class="user-name">
       captain_arroganto
      </strong>
     </span>
     <span class="highlight-separator">
      -
     </span>
     <span class="timestamp">
      Yesterday at 8:28 PM
     </span>
    </h2>
    <div class="message-text">
     <div class="btn-option">
     </div>
     <div class="btn-reaction">
     </div>
     <div class="markup">
      Hi all
     </div>
    </div>
   </div>
   <div class="accessory">
   </div>
  </div>
  <div class="message">
   <div class="body">
    <div class="message-text">
     <div class="btn-option">
     </div>
     <div class="btn-reaction">
     </div>
     <div class="markup">
      hi
     </div>
    </div>
   </div>
   <div class="accessory">
   </div>
  </div>
 </div>
</div>
<div class="divider">
 <div>
 </div>
 <span>
  January 7, 2018
 </span>
 <div>
 </div>
</div>
<div class="message-group hide-overflow">
 <div class="avatar-large stop-animation" style='background-image: url("/assets/0e291f67c9274a1abdddeb3fd919cbaa.png");'>
 </div>
 <div class="comment">
  <div class="message first">
   <div class="body">
    <h2 class="old-h2">
     <span class="username-wrapper">
      <strong class="user-name">
       captain_arroganto
      </strong>
     </span>
     <span class="highlight-separator">
      -
     </span>
     <span class="timestamp">
      Today at 8:49 AM
     </span>
    </h2>
    <div class="message-text">
     <div class="btn-option">
     </div>
     <div class="btn-reaction">
     </div>
     <div class="markup">
      hi
     </div>
    </div>
   </div>
   <div class="accessory">
   </div>
  </div>
 </div>
</div>
<div class="message-group hide-overflow">
 <div class="avatar-large stop-animation" style='background-image: url("/assets/0e291f67c9274a1abdddeb3fd919cbaa.png");'>
 </div>
 <div class="comment">
  <div class="message first">
   <div class="body">
    <h2 class="old-h2">
     <span class="username-wrapper">
      <strong class="user-name">
       captain_arroganto
      </strong>
     </span>
     <span class="highlight-separator">
      -
     </span>
     <span class="timestamp">
      Today at 9:32 AM
     </span>
    </h2>
    <div class="message-text">
     <div class="btn-option">
     </div>
     <div class="btn-reaction">
     </div>
     <div class="markup">
      hi there...
     </div>
    </div>
   </div>
   <div class="accessory">
   </div>
  </div>
 </div>
</div>
    
    """

    ProcessMessageBoard(sampleHTMLContent)
