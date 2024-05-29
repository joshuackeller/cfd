const handleSubmit = async (event) => {
  event.preventDefault();

  const question = document.getElementById("prompt-input")?.value;
  if (!question) return;

  const responseDiv = document.getElementById("response");
  const submitButton = document.getElementById("submit-button");
  responseDiv.innerHTML = Loader;
  submitButton.disabled = true;

  const result = await Call.post("/api/generate", {
    question,
  });

  responseDiv.innerHTML = result;
  submitButton.false = false;
};

class Call {
  static async get(url) {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Error getting data: ${response.status}`);
      }

      const text_data = await response.text();
      try {
        return JSON.parse(text_data);
      } catch {
        return text_data;
      }
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  static async post(url, data) {
    try {
      const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (!response.ok) {
        throw new Error(`Error posting data: ${response.status}`);
      }

      const text_data = await response.text();
      try {
        return JSON.parse(text_data);
      } catch {
        return text_data;
      }
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  static async put(url, data) {
    try {
      const response = await fetch(url, {
        method: "PUT",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (!response.ok) {
        throw new Error(`Error updating data: ${response.status}`);
      }

      const text_data = await response.text();
      try {
        return JSON.parse(text_data);
      } catch {
        return text_data;
      }
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  static async delete(url) {
    try {
      const response = await fetch(url, {
        method: "DELETE",
      });
      if (!response.ok) {
        throw new Error(`Error deleting data: ${response.status}`);
      }

      const text_data = await response.text();
      try {
        return JSON.parse(text_data);
      } catch {
        return text_data;
      }
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
}

const Loader = `
<div style="width: 100%; display: flex; justify-content: center; padding: 10px">
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="animate-spin lucide lucide-loader"><path d="M12 2v4"/><path d="m16.2 7.8 2.9-2.9"/><path d="M18 12h4"/><path d="m16.2 16.2 2.9 2.9"/><path d="M12 18v4"/><path d="m4.9 19.1 2.9-2.9"/><path d="M2 12h4"/><path d="m4.9 4.9 2.9 2.9"/></svg>
</div>
`;

// async function fetchStreamedData(url, data) {
//   // Initiate the fetch request
//   const responseDiv = document.getElementById("response");
//   const response = await fetch(url, {
//     method: "POST",
//     body: JSON.stringify(data),
//     headers: {
//       "Content-Type": "application/x-ndjson",
//     },
//   });

//   // Check if the response is OK
//   if (!response.ok) {
//     throw new Error(`HTTP error! Status: ${response.status}`);
//   }

//   // Get a reader from the response body
//   const reader = response.body.getReader();
//   const decoder = new TextDecoder("utf-8");
//   let ndjsonBuffer = "";

//   // Function to process each chunk of data
//   const processChunk = ({ done, value }) => {
//     if (done) {
//       console.log("Stream has been fully consumed.");
//       return;
//     }

//     // Decode the chunk to a string
//     ndjsonBuffer += decoder.decode(value, { stream: true });

//     // Split the buffer by newlines to get complete JSON objects
//     let lines = ndjsonBuffer.split("\n");

//     // The last line may not be a complete JSON object, so keep it in the buffer
//     ndjsonBuffer = lines.pop();

//     // Process each complete JSON line
//     lines.forEach((line) => {
//       if (line.trim().length > 0) {
//         try {
//           const obj = JSON.parse(line);
//           responseDiv.innerHTML += obj.response;

//           // Handle the JSON object here
//           // Example: append it to an array, display it in the UI, etc.
//         } catch (e) {
//           console.error("Error parsing JSON:", e);
//         }
//       }
//     });

//     // Read the next chunk
//     return reader.read().then(processChunk);
//   };

//   // Start reading the stream
//   reader.read().then(processChunk).catch(console.error);
// }
