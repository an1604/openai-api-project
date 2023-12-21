# Car Loan Bot README

## Overview of Modifications

### 1) Additions to `tool_chatbot` Package:

To enhance robustness and readability, new files were added:

#### 1.1) New Files:

- **`prompts.py`**: Stores prompts for prompt engineering to enhance model responses.
- **`exceptions.py`**: Organizes exceptions separately for improved code cleanliness.
- **`helper_functions.py`**: Houses overall helper functions used across multiple files to avoid circular imports.
- **`moderation.py`**: Contains a model to detect violating content in user input and act accordingly based on predictions. This addition serves to prevent prompt injection attacks by identifying and handling potentially harmful content in user inputs.

#### 1.2) `Loan_Process` Package:

- Essential files were added to improve the conversation process:
  - **`Car` Package:** Stores `car.py`, including an object called `CarDetails` that captures necessary car information.
  - **`Client` Package:** Contains three files for client information:
    - `clientInfo.py`: Stores financial information as `ClientInfo`.
    - `client_personal.py`: Holds personal information as `ClientPersonalInfo`.
    - `loan.py`: Manages necessary information for a car loan in the `Loan` object.
    - `client.py`: Aggregates all objects into a single `Client` object, facilitating information transfer to required functions.
  - **`Product_Predictions` Package:** Manages situations where the assistant needs to predict a suitable product for the client.
    - `decision_tree_classifier.py`: Stores the decision tree-based model and key steps in model building.
      - **Decision Tree Model:**
        - Predicts the best loan product based on client financial and personal data.
      - **Usage:**
        - Activated when a direct suitable loan product isn't found.
        - Analyzes client information to predict a closely matching loan product.
        - Guides the assistant in providing accurate and tailored recommendations.
        - The Primary goal is to predict the most suitable loan when no accurate match is found.
      - **Benefits:**
        - Improves user satisfaction by offering more relevant and personalized loan options.
        - Addresses scenarios where direct matches are unavailable, providing alternative recommendations.
        - Enhances the overall effectiveness of the car loan bot in assisting users with diverse financial needs.

### 2) Modifications in Existing Files:

#### 2.1) `chat_utills.py`:

- Added max tokens to the data dictionary to limit user input for efficiency and security.
- Broke down the `get_chat_answer` function into multiple cleaner functions:
  - `is_client_completed`: Checks if client info isn't complete.
  - `get_functions_after_remove`: Removes functions requiring incomplete client info.
  - `function_contains_in(response)`: Checks if a function is present in the response.
  - `get_available_functions`: Retrieves functions contained in the response.
  - `get_missing_arguments_from_function`: Extracts missing arguments from a function.
  - `is_message_contains_in(response)`: Checks if a message is present in the model response.
  - `call_function_recursively`: Recursively calls the function if no response is obtained, moving the try-catch block out for clarity.

#### 2.2) `chat_tools.py`:

- Added functions:
  - `check_for_available_products`: Checks for a suitable product based on client financial information.
  - `check_missing_data`: This function trying to keep the data collection flow after the assistance answered to an unrelated question. I saw that the model was having trouble keeping up the flow after that. 
  - `save_client_personal_information`: Saves client's personal information in the `Client` object.
  - `save_client_info`: Saves client's financial information in the `Client` object.
  - `save_car_details`: Saves client's car details for a car loan in the `Client` object.
  - `save_loan_details`: Stores loan details in the `Client` object after finding a suitable product.
  - `get_recommended_products`: Utilizes the decision tree model to find a closer suitable product if none is found.

### 3) Modifications in `prompts` Package:

Fine-tuned prompts for better model performance:
- Added `role.txt` for each user input to clarify the model's role and context.
- Added `GeneralConversationGuidelines.txt` for every user input to enhance conversation flow.
- Updated `v4_1ofer.txt` to align with project requirements.

### 4) Added fabricated dataset of car loans - `CL-programs.csv`.

### 5) Changed the `knowledgebase.csv` file according to car loan details.

### Note: 
All the conversation results are in `Conversations_Results` package, this package includes the three requested scenarios: 
Happy client scenario, Unhappy client scenario, and Doubting client scenario. For each scenario, you get two JSON files that represent two conversations and pictures that represent the chat itself.
