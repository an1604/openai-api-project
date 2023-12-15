import React, { useState } from 'react';
import { Picker } from 'emoji-mart';
import axios from 'axios';

const EmojiPickerUploader = () => {
  const [selectedEmoji, setSelectedEmoji] = useState(null);

  const handleEmojiSelect = (emoji) => {
    setSelectedEmoji(emoji);
  };

  const handleUploadEmoji = () => {
    if (selectedEmoji) {
      axios
        .post('/upload-emoji', { emoji: selectedEmoji })
        .then((response) => {
          console.log('Emoji uploaded successfully!');
        })
        .catch((error) => {
          console.error('Error uploading emoji: ', error);
        });
    }
  };

  return (
    <div>
      <h2>Emoji Picker and Uploader</h2>
      <Picker onSelect={handleEmojiSelect} />
      {selectedEmoji && (
        <div>
          <div>
            <img src={selectedEmoji.image} alt={selectedEmoji.id} />
          </div>
          <button onClick={handleUploadEmoji}>Upload Emoji</button>
        </div>
      )}
    </div>
  );
};

export default EmojiPickerUploader;
