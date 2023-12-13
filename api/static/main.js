const general_prompt = document.getElementById("general-prompt").ariaValueMax;
let server = ""
let data = {
  prompt: general_prompt
}
fetch(server, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => console.log(data))
.catch((error)=> console.error('Error: ', error))
