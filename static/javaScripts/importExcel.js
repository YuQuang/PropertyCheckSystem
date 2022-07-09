total_data = [];
// 當網站準備好時執行
$(document).ready(function(){
    
});

// 當檔案上傳時瀏覽檔案
$('#inputFile').on('change',(e)=>{

    // 檢查使用者是否有上傳檔案
    if(e.target.files.length >= 1){
        $('#fileName').text(e.target.files[0]['name']);
    }else{
        // 使用者取消上傳
        return 0;
    }
    
    // 先清除表格內html
    clearData();

    // 獲取上傳檔案
    var files = e.target.files;
    var fileReader = new FileReader();

    // 當讀入檔案時觸發
    fileReader.onload = function(ev) {
        try {
            // 取得檔案內容
            var data = ev.target.result
            // 將檔案以2進制讀取
            var workbook = XLSX.read(data, {
                type: 'binary'
            })
            // 儲存獲取到的資料
            var persons = [];
        } catch (e) {
            // 處理例外情況
            console.log('檔案型別不正確');
            return;
        }

        // 遍歷每張表讀取
        for (var sheet in workbook.Sheets) {
            if (workbook.Sheets.hasOwnProperty(sheet)) {
                persons = persons.concat(XLSX.utils.sheet_to_json(workbook.Sheets[sheet]));
                break;
            }
        }

        // 將解析到的表格資料交給Show函示呈現
        showExcel(persons);
    };

    // 以二進位制方式開啟檔案(此舉動將會觸發上面所指定的函式)
    fileReader.readAsBinaryString(files[0]);
    return 0;
});

// 當保存按鈕被按下時
$('#saveBtn').on('click',(e)=>{
    
    saveData();

});

// 當清除按鈕被按下時
$('#clearBtn').on('click',(e)=>{
    clearData();
});

// 呈現表格資料
function showExcel(data){
    // 暫時存放變數
    var is_checked, tip, unit, singleValue,
    position, deadline, number, brand,
    labelPosition, productName, productNumber;

    // 預覽表格內容
    var total_form = "";
    // 產品總價值
    var total_value = 0;
    // 產品總數
    var total_quantity = data.length;

    for(let i = 0;i < data.length;i++){
        /**
            對資料先做處理
            ，預防產生未知的錯誤，並過濾掉沒有數值的資料
        */
        is_checked    = data[i]['盤點'];
        if(is_checked == undefined) is_checked = "X";
        position      = data[i]['實際位置'];
        if(position == undefined) position = "";
        tip           = data[i]['備註'];
        if(tip == undefined) tip = "";
        labelPosition = data[i]['產貼位置地點'];
        if(labelPosition == undefined) labelPosition = "未知";
        productNumber = data[i]['財產編號'];
        if(productNumber == undefined) productNumber = "未知";
        number        = data[i]['序號'];
        if(number == undefined) number = "未知";
        productName   = data[i]['財產名稱'];
        if(productName == undefined) productName = "未知";
        brand         = data[i]['廠牌型式'];
        if(brand == undefined) brand = "未知";
        getDate       = data[i]['取得日期'];
        if(getDate == undefined) getDate = "未知";
        deadline      = data[i]['年限'];
        if(deadline == undefined) deadline = "未知";
        unit          = data[i]['單位'];
        if(unit == undefined) unit = "";
        quantity      = data[i]['數量'];
        if(quantity == undefined) quantity = 1;
        singleValue   = data[i]['單價'];
        if(singleValue == undefined) singleValue = "0";

        // 計算總價格，並過濾未知情況
        try{
            total_value += parseInt(quantity) * parseInt(singleValue.replace(",",""));
        }catch(e){
            console.log(i + "Can't to number");
        }
        
        total_form += "<tr>";
        
        // 產生表格html內容
        total_form += "<td>";
        if(is_checked == "V" || is_checked == "v"){
            total_form += "<img src='" + tick_img + "' width='30px' class='mx-auto'>";
        }else{
            total_form += "<img src='" + cross_img +  "' width='30px' class='mx-auto'>";
        }
        total_form += "</td>";

        total_form += "<td>" + position + "</td>";
        total_form += "<td>" + tip + "</td>";
        total_form += "<td>" + labelPosition + "</td>";
        total_form += "<td>" + productNumber + "</td>";
        total_form += "<td>" + number + "</td>";
        total_form += "<td>" + productName + "</td>";
        total_form += "<td>" + brand + "</td>";
        total_form += "<td>" + getDate + "</td>";
        total_form += "<td>" + deadline + "</td>";
        total_form += "<td>" + quantity + "</td>"; 
        total_form += "<td>" + unit + "</td>";
        total_form += "<td>" + singleValue + "</td>";
        total_form += "</tr>";

        // 將資料封裝成json檔案方便儲存
        total_data.push({
            "is_check": is_checked,
            "tip": tip,
            "position": position,
            "label_position": labelPosition,
            "product_number": productNumber,
            "product_name": productName,
            "number": number,
            "get_date": getDate,
            "quantity": quantity,
            "brand": brand,
            "age_limit": deadline,
            "unit": unit,
            "single_value": singleValue
        });
    }

    // 更新表格
    $("#form_content").html(total_form);
    // 更新總價格
    $("#total_value").text(total_value);
    // 更新總數量
    $("#total_quantity").text(total_quantity);

    return 0;
}

// 讀取Cookie
function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

// 保存資料
function saveData(){
    var csrftoken = readCookie("csrftoken");
    $.ajax({
        url: sava_url,
        type: "POST",
        dataType: 'json',
        data: {'data': JSON.stringify(total_data)},
        headers: {"X-CSRFToken": csrftoken},
        timeout: 20000,
        success: (res)=>{
            alert(res['result']);
            if(res['result'] == 'success'){
                console.log('print duplicate');
                console.log(res['duplicatelist']);
                mySocket.send(JSON.stringify({"action": "newNotify"}));
            }
        }
    });
}

// 清除資料
function clearData(){
    $('#form_content').html('');
    $('#total_quantity').html('');
    $('#total_value').html('');
}