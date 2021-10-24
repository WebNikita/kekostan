//selecting all required elements
const dropArea = document.querySelector(".drag-area"),
  dragText = dropArea.querySelector("header"),
  button = dropArea.querySelector("button"),
  input = dropArea.querySelector("input");

button.onclick = () => {
  input.click(); //if user click on the button then the input also clicked
};

input.addEventListener("change", function () {
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  sendFile(this);
});

//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event) => {
  event.preventDefault(); //preventing from default behaviour
  dragText.textContent = "Release them!";
});

//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", () => {
  dragText.textContent = "Move Here!";
});

//If user drop File on DropArea
dropArea.addEventListener("drop", (event) => {
  event.preventDefault(); //preventing from default behaviour
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  let str = "";
  let fileinp = event.dataTransfer.files;
  for (let i = 0; i < fileinp.length; i++) {
    str += (fileinp[i].name + "\n");
  }
  dropArea.textContent = str;
  sendFile(fileinp);
  // input.;
});
