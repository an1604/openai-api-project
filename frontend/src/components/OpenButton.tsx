import arrowIcon from '../assets/arrow.svg';

const OpenButton = ({
  setShowChatbot,
  showChatbot,
}: {
  setShowChatbot: React.Dispatch<React.SetStateAction<boolean>>;
  showChatbot: boolean;
}) => {
  const handleShowChatbot = () => {
    setShowChatbot(!showChatbot);
    const chatbotStatus = showChatbot ? 'chatbot-closed' : 'chatbot-open';
    window.parent.postMessage(chatbotStatus, '*');
  };

  return (
    <>
      <div className='button-container'>
        <button onClick={() => handleShowChatbot()}>
          <img
            src={arrowIcon}
            alt='My SVG'
            className='dropdown-button'
            style={{
              transform: showChatbot ? 'rotate(0deg)' : 'rotate(180deg)',
            }}
          />
        </button>
      </div>
    </>
  );
};

export default OpenButton;
