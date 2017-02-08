
$.extend({// 获取http请求参数
	getUrlVars : function() {
		var vars = [], hash;
		var hashes = window.location.href.slice(
				window.location.href.indexOf('?') + 1).split('&');
		for (var i = 0; i < hashes.length; i++) {
			hash = hashes[i].split('=');
			vars.push(hash[0]);
			vars[hash[0]] = hash[1];
		}
		return vars;
	},
	getUrlVar : function(name) {
		return $.getUrlVars()[name];
	}
});


/** ajax异步提交数据 */
function ajaxPost(param, action, successMethod) {
	$.ajax({
		type : "POST",
		url : action,
		dataType : "json",
		data : param,
		success : successMethod,
		error : function(XMLHttpRequest, textStatus, errorThrown) {
		}
	});
}
function log(data) {
	console.log(JSON.stringify(data))
}
function renderData(options, url) {
	$('#inparamJson').html(syntaxHighlight(options));
	url = url.replace("http://localhost:5002", "");
	$.ajax({
		type : "POST",
		url : url,
		dataType : "json",
		contentType : "application/json;charset=UTF-8",
		data : JSON.stringify(options),
		success : function(data) {
			$('#result').html(syntaxHighlight(data));
		},
		error : function(XMLHttpRequest, textStatus, errorThrown) {
		}
	});
}
function syntaxHighlight(json) {
	if (typeof json != 'string') {
		json = JSON.stringify(json, undefined, 2);
	}
	json = json.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>');
	return json
			.replace(
					/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
					function(match) {
						var cls = 'number';
						if (/^"/.test(match)) {
							if (/:$/.test(match)) {
								cls = 'key';
							} else {
								cls = 'string';
							}
						} else if (/true|false/.test(match)) {
							cls = 'boolean';
						} else if (/null/.test(match)) {
							cls = 'null';
						}
						return '<span class="' + cls + '">' + match + '</span>';
					});
}


function dataText() {
	var $inputForm = $("#inputForm");
	$inputForm.validate({
		rules: {
			code: "code",
			code3:"code",
			code2:"code2",
			code4:"code4",
			firstLetter: "firstLetter",
			locOrder: "digits",
			lng: "number",
			lat: "number"
		}
	});
	$.validator.addMethod("code",function(value,element){
		var check = /^[A-Z]{3}$/;
		return this.optional(element)||(check.test(value));
	},"三字码格式不正确");
	$.validator.addMethod("code3",function(value,element){
		var check = /^[A-Z]{3}$/;
		return this.optional(element)||(check.test(value));
	},"三字码格式不正确");
	$.validator.addMethod("code2",function(value,element){
		var check = /^[A-Z]{2}$/;
		return this.optional(element)||(check.test(value));
	},"二字码格式不正确");
	$.validator.addMethod("firstLetter",function(value,element){
		var check = /^[A-Z]{1}$/;
		return this.optional(element)||(check.test(value));
	},"首字母格式不正确");
	$.validator.addMethod("code4",function (value,element) {
		var check = /^[A-Z]{4}$/;
		return this.optional(element)||(check.test(value));
	},'四字码格式不正确');
}


var list = [];
var id;
var pageNum = 1;
var pageSize;
var pageList = 15;
var sortRules = 'asc';
var sortWord = 'id';
var certflag = false;

function page(num, str) {
	alert(num, str);
	alert()
	if (str) {
		pageNum = parseInt(num);
		console.log('页数', pageNum)
	} else {
		if (num == "first") {
			pageNum = 1;
		}
		if (num == "prev") {
			console.log(pageNum);
			if(pageNum <= 1){
				pageNum = 1;
				return false;
			}else {
				pageNum = pageNum - 1;
			}
		}
		if (num == "next") {
			if(pageNum >=pageSize){
				pageNum = pageSize;
				return false;
			}else {
				pageNum = pageNum + 1;
			}
			console.log("当前页数", pageNum);
			console.log("页数",pageSize)
		}
		if (num == "last") {
			pageNum = pageSize;
		}
	}
	$("#pageTo").val(pageNum); //显示当前是第几页
	init();
}

function sortData(field) {
	if (field == 'id') {
		sortWord = 'id';
	}
	if (field == 'name') {
		sortWord = 'name';
	}
	if (field == 'code') {
		sortWord = 'code';
	}
	if(field == 'firstLetter'){
		sortWord = 'firstLetter';
	}
	if (field == 'code4') {
		sortWord = 'code4';
	}
	if (field == 'areaType') {
		sortWord = 'areaType';
	}
	if(field == 'locOrder'){
		sortWord = 'locOrder';
	}
	if(field == 'title'){
		sortWord = 'title';
	}
	if (flag) {
		sortRules = 'asc';
	} else {
		sortRules = 'desc';
	}
	flag = !flag;
	//console.log(sortWord);

	init();
}

function jumpTo() {
	pageNum = parseInt($("#pageTo").val());
	init();
	return false;

}

// jQuery.extend(jQuery.validator.messages, {
// 	required: "必选字段",
// 	remote: "请修正该字段",
// 	email: "请输入正确格式的电子邮件",
// 	url: "请输入合法的网址",
// 	date: "请输入合法的日期",
// 	dateISO: "请输入合法的日期 (ISO).",
// 	number: "请输入合法的数字",
// 	digits: "只能输入整数",
// 	creditcard: "请输入合法的信用卡号",
// 	equalTo: "请再次输入相同的值",
// 	accept: "请输入拥有合法后缀名的字符串",
// 	maxlength: jQuery.validator.format("请输入一个长度最多是 {0} 的字符串"),
// 	minlength: jQuery.validator.format("请输入一个长度最少是 {0} 的字符串"),
// 	rangelength: jQuery.validator.format("请输入一个长度介于 {0} 和 {1} 之间的字符串"),
// 	range: jQuery.validator.format("请输入一个介于 {0} 和 {1} 之间的值"),
// 	max: jQuery.validator.format("请输入一个最大为 {0} 的值"),
// 	min: jQuery.validator.format("请输入一个最小为 {0} 的值")
// });

