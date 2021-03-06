let span = document.getElementById("telegram-code");
let files = [];
let mergeBtn = document.getElementById("merge-button");
let user_code;
document.addEventListener("DOMContentLoaded", () => {
  getCode();
});

function getCode() {
  let xhr = new XMLHttpRequest();

  url = "http://localhost:5000/pdfun/api/v1.0/get_code";
  // 2. Настраиваем его: GET-запрос по URL /article/.../load
  xhr.open("GET", url, true);
  xhr.responseType = "json";
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
      res = xhr.response;
      user_code = res["user_code"];
      console.log("user code:");
      console.log(user_code);

      span.textContent = user_code;
      console.log("files:");
      console.log(files);
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

mergeBtn.onclick = function () {
  if (files) {
    sendFile(files, "merge");
  } else {
    console.log("No file!");
  }
};

function setFile(input) {
  let inputFiles = input.files;
  console.log("inputFiles:");
  console.log(inputFiles);
  Array.prototype.forEach.call(inputFiles, (file) => files.push(file));
  console.log("files:");
  console.log(files);
}

function sendFile(input, funcType) {
  console.log(input);
  console.log(funcType);
  // 1. Создаём новый XMLHttpRequest-объект
  let xhr = new XMLHttpRequest();
  url = "http://localhost:5000/pdfun/api/v1.0/merge_files";
  // 2. Настраиваем его: GET-запрос по URL /article/.../load
  xhr.open("POST", url);

  // 3. Отсылаем запрос
  let formData = new FormData();
  //   formData.append("user_code", user_code);
  //   formData.append("files", files[user_code]);
  console.log(user_code);
  for (let i = 0; i < files.length; i++) {
    formData.append(user_code, files[i]);
  }
  console.log("formData");
  console.log(formData);
  xhr.send(formData);

  // 4. Этот код сработает после того, как мы получим ответ сервера
  xhr.onload = function () {
    if (xhr.status != 200) {
      // анализируем HTTP-статус ответа, если статус не 200, то произошла ошибка
      console.log(`Ошибка ${xhr.status}: ${xhr.statusText}`); // Например, 404: Not Found
    } else {
      // если всё прошло гладко, выводим результат
      console.log(xhr.response);
      console.log(`Готово, получили ${xhr.response.length} байт`); // response -- это ответ сервера
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
  files = [];
}
