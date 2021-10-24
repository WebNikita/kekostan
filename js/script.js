let telegramCode = document.getElementById("telegram-code");
let files = [];
let mergeBtn = document.getElementById("merge-button");
let flipBtn = document.getElementById("flip-button");
let splitBtn = document.getElementById("split-button");
let telegramBtn = document.getElementById("telegram-button");
let userCode;
// let convertButton = document.getElementById("convert-button");

//selecting all required elements
let dropArea = document.querySelector(".drag-area");
let dragText = dropArea.querySelector("header");
let browseButton = document.getElementById("browse-button");
let clearButton = document.getElementById("clear-button");
let fileInput = document.getElementById("file-input");

document.addEventListener("DOMContentLoaded", () => {
  getCode();
  console.log("DOM fully loaded and parsed");
});

// convertButton.addEventListener("click", getCode);

mergeBtn.onclick = function () {
  if (files.length) {
    sendFile("merge");
  } else {
    alert("No file uploaded!");
  }
};

telegramBtn.onclick = () => {
  if (files.length) {
    sendFile("flip");
  } else {
    alert("No file uploaded!");
  }
};

clearButton.onclick = () => {
  files = [];
  dragText.textContent = "Drag & Drop to Upload File";
};

browseButton.onclick = () => {
  fileInput.click();
  //if user click on the browseButton then the input also clicked
};
flipBtn.onclick = () => {
  sendFile("flip");
};

splitBtn.onclick = () => {
  sendFile("split");
};

fileInput.addEventListener("change", function () {
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  let fileinp = this.files;
  setFile(fileinp);
});

// //If user Drag File Over DropArea
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
  let fileInp = event.dataTransfer.files;
  console.log(typeof fileInp);
  if (
    Array.prototype.every.call(fileInp, (file) => file.name.endsWith(".pdf"))
  ) {
    setFile(fileInp);
  } else {
    dragText.textContent = "Drag & Drop to Upload File";
    alert("Uploading files should be .pdf format");
  }
});

function getCode() {
  let xhr = new XMLHttpRequest();

  url = "http://localhost:5000/pdfun/api/v1.0/get_code";
  // 2. Настраиваем его: GET-запрос по URL /article/.../load
  xhr.open("GET", url, true);

  xhr.send();

  // 4. Этот код сработает после того, как мы получим ответ сервера
  xhr.onload = function () {
    if (xhr.status != 200) {
      // анализируем HTTP-статус ответа, если статус не 200, то произошла ошибка
      console.log(`Ошибка ${xhr.status}: ${xhr.statusText}`); // Например, 404: Not Found
    } else {
      // если всё прошло гладко, выводим результат
      console.log("xhr.response:");
      console.log(xhr.response.toString());
      console.log(`Готово, получили ${xhr.response.length} байт`); // response -- это ответ сервера
      res = JSON.parse(xhr.response);
      userCode = res["user_code"];
      console.log("user code:");
      console.log(userCode);

      telegramCode.textContent = userCode;
      console.log("files:");
      console.log(files);
    }
  };
}

function setFile(inputFiles) {
  // let inputFiles = fileInput.files;
  console.log("inputFiles from setFile:");
  console.log(inputFiles);
  Array.prototype.forEach.call(inputFiles, (inputFile) => {
    if (files.every((file) => file.name !== inputFile.name)) {
      files.push(inputFile);
    } else {
      alert(`${inputFile.name} already uploaded!`);
    }
  });
  console.log("files:");
  console.log(files);
  dragText.textContent = "";
  let node = document.createElement("ul");

  dragText.appendChild(node);
  for (let i = 0; i < files.length; i++) {
    let li = document.createElement("li");
    li.textContent = files[i].name;
    node.appendChild(li);
  }
}

function sendFile(funcType) {
  if (funcType === "merge" && files.length < 2) {
    alert("For merge there are should be at least 2 files!");
    return 1;
  }
  if (funcType === "split" && files.length !== 1) {
    alert("For split there is should be only 1 file!");
    return 1;
  }
  req_dict = { flip: "flip_pages", merge: "merge_files", split: "split_pages" };

  // 1. Создаём новый XMLHttpRequest-объект
  let xhr = new XMLHttpRequest();
  console.log(req_dict[funcType]);
  url = `http://localhost:5000/pdfun/api/v1.0/${req_dict[funcType]}`;
  // 2. Настраиваем его: GET-запрос по URL /article/.../load
  xhr.open("POST", url);

  xhr.responseType = "blob";
  // xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  // 3. Отсылаем запрос
  let formData = new FormData();
  //   formData.append("user_code", user_code);
  //   formData.append("files", files[user_code]);
  console.log(userCode);
  for (let i = 0; i < files.length; i++) {
    formData.append(userCode, files[i]);
  }
  console.log("formData");
  console.log(formData);
  xhr.send(formData);
  xhr.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      if (funcType === "merge") {
        returnName = "merged.pdf";
        blobType = "application/pdf";
      } else if (funcType === "flip") {
        returnName = "rotated.zip";
        blobType = "application/zip";
      } else if (funcType === "split") {
        returnName = "splitted.zip";
        blobType = "application/zip";
      }
      var blob = new Blob([this.response], { type: blobType });
      var url = window.URL.createObjectURL(blob);
      var link = document.createElement("a");
      document.body.appendChild(link);
      link.style = "display: none";
      link.href = url;
      link.download = returnName;
      link.click();

      setTimeout(() => {
        window.URL.revokeObjectURL(url);
        link.remove();
      }, 100);
    }
  };

  xhr.onerror = function () {
    console.log("Запрос не удался");
  };
  files = [];
  dragText.textContent = "Drag & Drop to Upload File";
}

function getFileFromTg() {
  let xhr = new XMLHttpRequest();

  url = "http://localhost:5000/pdfun/api/v1.0/get_file_from_tg";
  // 2. Настраиваем его: GET-запрос по URL /article/.../load
  xhr.open("POST", url, true);
  userCodeJson = JSON.stringify({ user_code: userCode });
  console.log(userCodeJson);
  console.log(typeof userCodeJson);
  xhr.send(userCodeJson);

  // 4. Этот код сработает после того, как мы получим ответ сервера
  xhr.onload = function () {
    if (xhr.status != 200) {
      // анализируем HTTP-статус ответа, если статус не 200, то произошла ошибка
      console.log(`Ошибка ${xhr.status}: ${xhr.statusText}`); // Например, 404: Not Found
    } else {
      // если всё прошло гладко, выводим результат
      console.log("xhr.response:");
      console.log(xhr.response.toString());
      console.log(`Готово, получили ${xhr.response.length} байт`); // response -- это ответ сервера
      // res = JSON.parse(xhr.response);
      // user_code = res["user_code"];
      // console.log("user code:");
      // console.log(user_code);

      // span.textContent = user_code;
      // console.log("files:");
      // console.log(files);
    }
  };

  xhr.onprogress = function (event) {
    if (event.lengthComputable) {
      console.log(`Получено ${event.loaded} из ${event.total} байт`);
    } else {
      console.log(`Получено ${event.loaded} байт`); // если в ответе нет заголовка Content-Length
    }
  };

  xhr.onerror = function () {
    console.log("Запрос не удался");
  };
}
