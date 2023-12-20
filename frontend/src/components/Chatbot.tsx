import { useState, useRef, useEffect, Dispatch, SetStateAction } from 'react';
import userDemoImage from '../assets/user_image.png';
import sendArrow from '../assets/send-arrow.svg';
import emojiIcon from '../assets/emoji.svg';
import fileAttachment from '../assets/file-attachment.svg';
import EmojiPicker, { EmojiStyle } from 'emoji-picker-react';
import DOMPurify from 'dompurify';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

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

type ColorCode = {
  color1: string;
  color2: string;
};

const backendUrl = import.meta.env.VITE_BACKEND_URL;

const Chatbot = ({
  showChatbot,
  chatHistory,
  setChatHistory,
  currentUser,
  currentLanguage,
  setCurrentUser,
  hasSentFirstMessage,
  setHasSentFirstMessage,
  waitingForBotReply,
  setWaitingForBotReply,
}: {
  showChatbot: boolean;
  chatHistory: ChatMessage[];
  setChatHistory: Dispatch<SetStateAction<ChatMessage[]>>;
  currentUser: string;
  currentLanguage: ChatLanguage;
  setCurrentUser: Dispatch<SetStateAction<string>>;
  hasSentFirstMessage: boolean;
  setHasSentFirstMessage: Dispatch<SetStateAction<boolean>>;
  waitingForBotReply: boolean;
  setWaitingForBotReply: Dispatch<SetStateAction<boolean>>;
}) => {
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [colorCode, setColorCode] = useState<ColorCode>({
    color1: '#0084da',
    color2: '#06bff5',
  });
  const [chobotSize, setChobotSize] = useState('lg');
  const [userImage, setuserImage] = useState(userDemoImage);

  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!hasSentFirstMessage && currentUser !== '') {
      setHasSentFirstMessage(true);
      handleFirstMessage();
    }
  }, [currentUser, hasSentFirstMessage]);

  const handleEmojiUploader = (emojiData: any) => {
    setInputValue(
      (prevInputValue) =>
        prevInputValue +
        (emojiData.isCustom ? emojiData.unified : emojiData.emoji)
    );
    setShowEmojiPicker(false);
  };

  const setCurrentTime = () => {
    const currentTime = new Date();
    const hours = currentTime.getHours();
    const minutes = currentTime.getMinutes();
    const amOrPm = hours >= 12 ? 'PM' : 'AM';
    const formattedHours = hours > 12 ? hours - 12 : hours;
    const formattedMinutes = minutes < 10 ? '0' + minutes : minutes;
    const formattedTime = `${formattedHours}:${formattedMinutes} ${amOrPm}`;
    return formattedTime;
  };

  const handleFirstMessage = async () => {
    setWaitingForBotReply(true);
    const newUserMessage = {
      text: '',
      pov: 'user',
      time: '',
    };
    await getBotReply(newUserMessage, chatHistory);
  };

  const handleUserInput = async (userMessage: string) => {
    if (userMessage !== '') {
      const formattedTime = setCurrentTime();
      const newUserMessage = {
        text: userMessage,
        pov: 'user',
        time: formattedTime,
      };
      const newChatHistory = [...chatHistory, newUserMessage];
      setChatHistory(newChatHistory);
      setInputValue('');
      setWaitingForBotReply(true);
      await getBotReply(newUserMessage, newChatHistory);
    }
  };

  const getBotReply = async (
    userMessage: ChatMessage,
    newChatHistory: ChatMessage[]
  ) => {
    try {
      const response = await axios.post(`${backendUrl}/send_local_hebrew_cd`, {
        Body: userMessage.text,
        WaId: currentUser,
      });

      const botReply = response.data;

      if (botReply !== '') {
        const formattedTime = setCurrentTime();
        const newBotMessage = {
          text: botReply,
          pov: 'partner',
          time: formattedTime,
        };
        setWaitingForBotReply(false);
        setChatHistory([...newChatHistory, newBotMessage]);
      }
    } catch (error: any) {
      setWaitingForBotReply(false);
      toast.error(error.response.data);
    }
  };

  const handleImageUpload = (event: any) => {
    const file = event.target.files[0];

    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        if (e.target === null) return;
        const base64Image = e.target.result;

        const currentTime = new Date();
        const hours = currentTime.getHours();
        const minutes = currentTime.getMinutes();
        const amOrPm = hours >= 12 ? 'PM' : 'AM';
        const formattedHours = hours > 12 ? hours - 12 : hours;
        const formattedMinutes = minutes < 10 ? '0' + minutes : minutes;
        const formattedTime = `${formattedHours}:${formattedMinutes} ${amOrPm}`;

        const newChatEntry = {
          text: inputValue,
          image: base64Image, // Store the base64 image in the chat entry
          pov: 'user',
          time: formattedTime,
        };

        setChatHistory([...chatHistory, newChatEntry]);
        setInputValue('');
      };
      reader.readAsDataURL(file);
    }
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory]);

  // Temprarly Code Start

  useEffect(() => {
    const url = new URL(window.location.href);
    const dirParam = url.searchParams.get('dir');
    const color1Param = url.searchParams.get('color1');
    const color2Param = url.searchParams.get('color2');
    const sizeParam = url.searchParams.get('size');
    const userImage = url.searchParams.get('image');
    if (dirParam && document.querySelector('html') !== null)
      document.querySelector('html')?.setAttribute('dir', dirParam);
    setColorCode({
      color1:
        color1Param && typeof color1Param === 'string'
          ? '#' + color1Param
          : '#0084da',
      color2:
        color2Param && typeof color1Param === 'string'
          ? '#' + color2Param
          : '#06bff5',
    });
    setChobotSize(sizeParam === 'lg' ? 'lg' : sizeParam === 'md' ? 'md' : 'lg');
    userImage && setuserImage(userImage);
    if (!currentUser) {
      const uid = Math.floor(Math.random() * 1000000000).toString();
      setCurrentUser(uid);
    }
  }, []);

  const gradientBackground = () => {
    if (colorCode.color1 && colorCode.color2) {
      return `linear-gradient(270deg, ${colorCode.color1} 0%, ${colorCode.color2})`;
    } else if (colorCode.color1) {
      return colorCode.color1;
    } else if (colorCode.color2) {
      return colorCode.color2;
    } else {
      return undefined;
    }
  };

  return (
    <>
      <div
        className={`main-container ${
          showChatbot ? 'active' : ''
        } ${chobotSize}`}
      >
        <div
          className='header'
          style={{
            background: gradientBackground(),
          }}
        >
          <div className='header-sub-container'>
            <div className='image-container'>
              <img src={userImage} alt='' />
            </div>
            <div className='user-details'>
              <h1>{currentLanguage.user_name}</h1>
              <p>{currentLanguage.availability}</p>
            </div>
          </div>
        </div>
        <div className='online-status-container'>
          <svg
            xmlns='http://www.w3.org/2000/svg'
            width='8'
            height='8'
            viewBox='0 0 8 8'
            fill='none'
          >
            <circle cx='4.26658' cy='4.23912' r='3.69334' fill='#02C75D' />
          </svg>
          <p>{currentLanguage.online_now}</p>
        </div>
        <div className='chatting-container' ref={chatContainerRef}>
          {chatHistory.map((chat, index) => {
            if (chat.pov === 'user') {
              return (
                <div
                  className='chatbot-reply'
                  key={index}
                  style={{ background: gradientBackground() }}
                >
                  <b
                    className='chatbot-arrow'
                    style={{ borderColor: colorCode.color1 }}
                  ></b>
                  <p> {chat.text}</p>

                  {chat?.image && (
                    // eslint-disable-next-line jsx-a11y/img-redundant-alt
                    <img
                      src={DOMPurify.sanitize(userImage)}
                      alt='Selected Image'
                      width='200'
                      className='uploaded-image'
                    />
                  )}

                  <span>{chat.time}</span>
                </div>
              );
            } else {
              return (
                <div className='chatting-sub-container' key={index}>
                  <div
                    className='image-container chatting-user'
                    style={{ borderColor: colorCode.color1 }}
                  >
                    <img src={userImage} alt='' />
                  </div>
                  <div className='message'>
                    <p>{chat.text}</p>

                    <span>{chat.time}</span>
                  </div>
                </div>
              );
            }
          })}

          {waitingForBotReply ? (
            <>
              <div className='chatting-sub-container'>
                <div className='image-container chatting-user'>
                  <img src={userImage} alt='' />
                </div>
                <div className='chat-bubble'>
                  <div className='typing'>
                    <div
                      className='dot'
                      style={{ backgroundColor: colorCode.color1 }}
                    ></div>
                    <div
                      className='dot'
                      style={{ backgroundColor: colorCode.color1 }}
                    ></div>
                    <div
                      className='dot'
                      style={{ backgroundColor: colorCode.color1 }}
                    ></div>
                  </div>
                </div>
              </div>
            </>
          ) : (
            ''
          )}
        </div>

        <div className='bottom-container'>
          <label htmlFor='image_upload' className='file-attachment'>
            <img src={fileAttachment} alt='' />
          </label>
          <input id='image_upload' type='file' onChange={handleImageUpload} />

          <button
            className='emoji-button'
            onClick={() => setShowEmojiPicker(!showEmojiPicker)}
          >
            <img src={emojiIcon} alt='' />
          </button>

          {showEmojiPicker && (
            <EmojiPicker
              onEmojiClick={handleEmojiUploader}
              autoFocusSearch={false}
              emojiStyle={EmojiStyle.NATIVE}
            />
          )}

          <input
            type='text'
            className='user-input'
            placeholder={currentLanguage.message}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.code === 'Enter') {
                e.preventDefault();
                handleUserInput(inputValue);
              }
            }}
          />
          <button
            className='send-message'
            onClick={() => {
              handleUserInput(inputValue);
            }}
            style={{ background: gradientBackground() }}
          >
            <img src={sendArrow} alt='' />
          </button>
        </div>
        <ToastContainer autoClose={5000} theme='light' />
      </div>
    </>
  );
};

export default Chatbot;
