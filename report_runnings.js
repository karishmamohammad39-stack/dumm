exports.header = null;

function toRoman(num) {
  var roman = { m: 1000, cm: 900, d: 500, cd: 400, c: 100, xc: 90, l: 50, xl: 40, x: 10, ix: 9, v: 5, iv: 4, i: 1 };
  var str = '';
  for (var key in roman) {
    var q = Math.floor(num / roman[key]);
    num -= q * roman[key];
    str += key.repeat(q);
  }
  return str;
}

exports.footer = {
  height: "0.6in",
  contents: function(pageNum, numPages) {
    // Pages 1 to 7 are preliminary pages (roman numerals: i, ii, iii, iv, v, vi, vii)
    if (pageNum <= 7) {
      return "<div style='text-align:center; font-family: \"Times New Roman\", serif; font-size: 11pt; color: #111;'>" + toRoman(pageNum) + "</div>";
    }
    // Main report body starts at page 8 (arabic numerals: 1, 2, 3...)
    var bodyPage = pageNum - 7;
    return "<div style='text-align:center; font-family: \"Times New Roman\", serif; font-size: 11pt; color: #111;'>" + bodyPage + "</div>";
  }
};
