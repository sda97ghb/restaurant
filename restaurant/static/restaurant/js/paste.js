let taskIdElem = $("#taskId");
let statusElem = $("#status");
let resultElem = $("#result");

let error = $("#error");

function displayError(err) {
    error.text(err);
}

function runPaste(createPasteEndpoint, pasteStatusEndpoint) {
    $.post(createPasteEndpoint)
        .done(function (taskId) {
            let timerId = setInterval(function () {
                $.getJSON(pasteStatusEndpoint.replace("task_id_placeholder", taskId))
                    .done(function (data) {
                        taskIdElem.text(data["id"]);
                        statusElem.text(data["status"]);
                        resultElem.text(data["result"]);
                        if (data["status"] === "SUCCESS" || data["status"] === "FAILURE") {
                            clearInterval(timerId);
                        }
                        if (data["status"] === "SUCCESS") {
                            let url = data["result"];
                            resultElem.html(`<a href="${url}">${url}</a>`);
                        }
                    })
                    .fail(displayError);
            }, 1000);
        })
        .fail(displayError);
}
