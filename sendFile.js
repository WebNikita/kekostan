let file = null;
let mergeBtn = document.getElementById("merge-button");
mergeBtn.onclick = function () {
  if (file !== null) {
    sendFile(file, "merge");
  } else {
    alert("No file!");
  }
};
function setFile(input) {
  file = input.files[0];

  console.log(`File name: ${file.name}`); // например, my.png
  console.log(`Last modified: ${file.lastModified}`); // например, 1552830408824
}
function sendFile(input, funcType) {
  console.log(input);
  console.log(funcType);
  // 1. Создаём новый XMLHttpRequest-объект
  let xhr = new XMLHttpRequest();

  url = "http://10.11.8.164:80/pdfun/api/v1.0/merge_files";
  // 2. Настраиваем его: GET-запрос по URL /article/.../load
  xhr.open("POST", "/article/xmlhttprequest/example/load");

  // 3. Отсылаем запрос
  xhr.send();

  // 4. Этот код сработает после того, как мы получим ответ сервера
  xhr.onload = function () {
    if (xhr.status != 200) {
      // анализируем HTTP-статус ответа, если статус не 200, то произошла ошибка
      alert(`Ошибка ${xhr.status}: ${xhr.statusText}`); // Например, 404: Not Found
    } else {
      // если всё прошло гладко, выводим результат
      alert(`Готово, получили ${xhr.response.length} байт`); // response -- это ответ сервера
    }
  };

  xhr.onprogress = function (event) {
    if (event.lengthComputable) {
      alert(`Получено ${event.loaded} из ${event.total} байт`);
    } else {
      alert(`Получено ${event.loaded} байт`); // если в ответе нет заголовка Content-Length
    }
  };

  xhr.onerror = function () {
    alert("Запрос не удался");
  };
  //alert(`File name: ${file.name}`); // например, my.png
  //alert(`Last modified: ${file.lastModified}`); // например, 1552830408824
}
