window.onload = function () {
    var min_date_dom = document.getElementById('min-date')
    var max_date_dom = document.getElementById('max-date')


    min_date_dom.onchange = function () {
        var value = min_date_dom.value
        if (!check_date(value)){
            alert("日期不合法，请按照年-月-日的格式输入")
        }
    }

    max_date_dom.onchange = function () {
        var value = max_date_dom.value
        if (!check_date(value)){
            alert("日期不合法，请按照年-月-日的格式输入")
        }
    }
}

    var match_str = "\\d{4}-\\d{2}-\\d{2}"



function check_date(value) {

    var reg = new RegExp("^(?:(?!0000)[0-9]{4}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-8])|(?:0[13-9]|1[0-2])-(?:29|30)|(?:0[13578]|1[02])-31)|(?:[0-9]{2}(?:0[48]|[2468][048]|[13579][26])|(?:0[48]|[2468][048]|[13579][26])00)-02-29)$")
    if (reg.test(value)){
        return true
    }
    return false
}


function on_submit(){
    var min_date_dom = document.getElementById('min-date')
    var max_date_dom = document.getElementById('max-date')
    console.log("check!")
    if (!check_date(min_date_dom.value) || !check_date(max_date_dom.value)){
        alert("日期不合法，请按照年-月-日的格式输入")
        return false;
    }
    return true
}

function check_submit(){
    if (on_submit()){
        document.getElementById("form").submit()
    }
}