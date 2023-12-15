# Leumi Chat Widget Integration
This is a script which simply brings a chat button, which toggles chat window in any html website.


##### To view live demo [click here](https://leumi.netlify.app/chat-widget).

## Steps For Installation
1. Add script to your website at the bottom of `body` tag in your HTML. 
   ```
     <script src="https://leumi.netlify.app/chat-widget.js"></script>
   ```
2. Now, we need to initialize the chat widget using below code.
    ```
      <script>
        // Initiliaze the chat
        new LeumiChat({});
      </script>
    ```
3. Boom! Widget should be visible on the bottom right side of the website.


## Customisation
Chat Widget  provide some customisation options which could be passed in the constuctor like below:-
```
 <script>
    // Initiliaze the chat
    new LeumiChat({
        gradientColor1: "####",
        gradientColor2: "####",
        .....
    });
  </script>
```

#### Available Options
| Key | Description | Available Options |
| ----------- | ----------- | --------- |
| `gradientColor1` | First  color for the main gradient in the widget | hexColor |
| `gradientColor2` | Second  color for the main gradient in the widget | hexColor |
| `size` | Size of the widget | `lg`, `md` |
| `image` | Add link of user image  | `CDN` |
| `dimension` | To change any dimension or space  | `object` |



### Options in dimension

| Key | Description | Available Options |
| ----------- | ----------- | --------- |
| `chatBoxSize` | Customize height width of chat widget | object |

Example of `chatBoxSize`:-
```
 <script>
    // Initiliaze the chat
    new LeumiChat({
      dimension: {
        chatBoxSize: {
          width: 380, // add custom width
          height: 550 // add custom height
        },
      }
    });
  </script>
```

| Key | Description | Available Options |
| ----------- | ----------- | --------- |
| `chatBoxPosition` | Customize position of chat widget in desktop & mobile | object |

Example of `chatBoxPosition`:-
```
 <script>
    // Initiliaze the chat
    new LeumiChat({
      dimension: {
        chatBoxPosition: {
          desktop: { // customize positions for desktop view
            right: 30, // add right space 
            bottom: 120 // add bottom space
          },
          mobile: {
            right: 10, // add right space 
            bottom: 80 // add bottom space
          }
        },
      }
    });
  </script>
```

| Key | Description | Available Options |
| ----------- | ----------- | --------- |
| `chatButtonPosition` | Customize position of chat button in desktop & mobile| object |

Example of `chatButtonPosition`:-
```
 <script>
    // Initiliaze the chat
    new LeumiChat({
      dimension: {
        chatButtonPosition: {
          desktop: { // customize positions for desktop view
            right: 30, // add right space 
            bottom: 30 // add bottom space
          },
          mobile: { // customize positions for mobile view
            right: 15, // add right space 
            bottom: 15 // add bottom space
          }
        }
      }
    });
  </script>
```
