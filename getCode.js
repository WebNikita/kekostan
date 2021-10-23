let span = document.getElementById("code-span");
let btn = document.getElementById("gen-code");
btn.addEventListener("click", getCode, false);

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
      console.log(xhr.response);
      console.log(`Готово, получили ${xhr.response.length} байт`); // response -- это ответ сервера
      res = xhr.response;
      span.textContent = res["User_code"];
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
