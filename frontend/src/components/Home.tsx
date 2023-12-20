import { useState, useEffect } from 'react';
import OpenButton from './OpenButton';
import Chatbot from './Chatbot';
import languageEn from '../data/languageEn.json';
import languageHe from '../data/languageHe.json';

type ChatMessage = {
  pov: string;
  image?: any;
  text: string;
  time: string;
};

type ChatLanguage = {
  user_name: string;
  availability: string;
  online_now: string;
  message: string;
};

const language = import.meta.env.VITE_CURRENT_LANGUAGE;

const Home = () => {
  const [showChatbot, setShowChatbot] = useState(false);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [currentUser, setCurrentUser] = useState<string>('');
  const [hasSentFirstMessage, setHasSentFirstMessage] = useState(false);
  const [waitingForBotReply, setWaitingForBotReply] = useState(false);
  const [currentLanguage, setCurrentLanguage] = useState<ChatLanguage>(
    language === 'hebrew' ? languageHe : languageEn
  );

  useEffect(() => {
    if (language === 'hebrew') {
      document.querySelector('html')?.setAttribute('dir', 'rtl');
      setCurrentLanguage(languageHe);
    } else {
      setCurrentLanguage(languageEn);
    }
  }, []);

  return (
    <div>
      {showChatbot && (
        <Chatbot
          showChatbot={showChatbot}
          chatHistory={chatHistory}
          setChatHistory={setChatHistory}
          currentUser={currentUser}
          setCurrentUser={setCurrentUser}
          currentLanguage={currentLanguage}
          hasSentFirstMessage={hasSentFirstMessage}
          setHasSentFirstMessage={setHasSentFirstMessage}
          waitingForBotReply={waitingForBotReply}
          setWaitingForBotReply={setWaitingForBotReply}
        />
      )}
      <OpenButton showChatbot={showChatbot} setShowChatbot={setShowChatbot} />
    </div>
  );
};

export default Home;
