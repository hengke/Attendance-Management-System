//****************针对第一种方式的具体js实现部分******************//
//****************所使用的数据是city.js******************//
//*https://github.com/visugar/FrontEnd-examples*//

/*根据id获取对象*/
//会影响其他js文件中使用$()
// function $(str) {
//     return document.getElementById(str);
// }

var addrShow = document.getElementById('destination');
var but = document.getElementsByClassName('met1')[0];
var prov = document.getElementById('prov');
var city = document.getElementById('city');
var country = document.getElementById('country');


/*用于保存当前所选的省市区*/
var current_region = {
    prov: '',
    city: '',
    country: ''
};

/*自动加载省份列表*/
(function showProv() {
    but.disabled = true;
    var len = provice.length;
    for (var i = 0; i < len; i++) {
        var provOpt = document.createElement('option');
        provOpt.innerText = provice[i]['name'];
        provOpt.value = i;
        prov.appendChild(provOpt);
    }
})();

/*根据所选的省份来显示城市列表*/
function showCity(obj) {
    var val = obj.options[obj.selectedIndex].value;
    if (val !== current_region.prov) {
        current_region.prov = val;
        addrShow.value = '';
        but.disabled = true;
    }
    //console.log(val);
    if (val != null) {
        city.length = 1;
        var cityLen = provice[val]["city"].length;
        for (var j = 0; j < cityLen; j++) {
            var cityOpt = document.createElement('option');
            cityOpt.innerText = provice[val]["city"][j].name;
            cityOpt.value = j;
            city.appendChild(cityOpt);
        }
    }
}

/*根据所选的城市来显示县区列表*/
function showCountry(obj) {
    var val = obj.options[obj.selectedIndex].value;
    current_region.city = val;
    if (val != null) {
        country.length = 1; //清空之前的内容只留第一个默认选项
        var countryLen = provice[current_region.prov]["city"][val].districtAndCounty.length;
        if(countryLen === 0){
            addrShow.value = provice[current_region.prov].name + '-' + provice[current_region.prov]["city"][current_region.city].name;
            return;
        }
        for (var n = 0; n < countryLen; n++) {
            var countryOpt = document.createElement('option');
            countryOpt.innerText = provice[current_region.prov]["city"][val].districtAndCounty[n];
            countryOpt.value = n;
            country.appendChild(countryOpt);
        }
    }
}

/*选择县区之后的处理函数*/
function selecCountry(obj) {
    current_region.country = obj.options[obj.selectedIndex].value;
    if ((current_region.city != null) && (current_region.country != null)) {
        but.disabled = false;
    }
}

/*点击确定按钮显示用户所选的地址*/
function showAddr() {
    addrShow.value = provice[current_region.prov].name + '-' + provice[current_region.prov]["city"][current_region.city].name + '-' + provice[current_region.prov]["city"][current_region.city].districtAndCounty[current_region.country];
}