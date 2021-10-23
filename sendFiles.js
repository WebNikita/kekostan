let files = [];
let mergeBtn = document.getElementById("merge-button");
mergeBtn.onclick = function () {
  if (files) {
    sendFile(files, "merge");
  } else {
    console.log("No file!");
  }
};
function setFile(input) {
  let file = input.files[0];
  files.push(file);
  console.log(files);
  console.log(`File name: ${file.name}`); // например, my.png
  console.log(`Last modified: ${file.lastModified}`); // например, 1552830408824
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
  for (let i in files) {
    console.log(i);
    formData.append("uploads", files[i]);
  }
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
  //console.log(`File name: ${file.name}`); // например, my.png
  //console.log(`Last modified: ${file.lastModified}`); // например, 1552830408824
}
