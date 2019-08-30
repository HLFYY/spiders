var n, r;
n = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
r = {
    rotl: function(e, t) {
        return e << t | e >>> 32 - t
    },
    rotr: function(e, t) {
        return e << 32 - t | e >>> t
    },
    endian: function(e) {
        if (e.constructor == Number)
            return 16711935 & r.rotl(e, 8) | 4278255360 & r.rotl(e, 24);
        for (var t = 0; t < e.length; t++)
            e[t] = r.endian(e[t]);
        return e
    },
    randomBytes: function(e) {
        for (var t = []; e > 0; e--)
            t.push(Math.floor(256 * Math.random()));
        return t
    },
    bytesToWords: function(e) {
        for (var t = [], n = 0, r = 0; n < e.length; n++,
        r += 8)
            t[r >>> 5] |= e[n] << 24 - r % 32;
        return t
    },
    wordsToBytes: function(e) {
        for (var t = [], n = 0; n < 32 * e.length; n += 8)
            t.push(e[n >>> 5] >>> 24 - n % 32 & 255);
        return t
    },
    bytesToHex: function(e) {
        for (var t = [], n = 0; n < e.length; n++)
            t.push((e[n] >>> 4).toString(16)),
            t.push((15 & e[n]).toString(16));
        return t.join("")
    },
    hexToBytes: function(e) {
        for (var t = [], n = 0; n < e.length; n += 2)
            t.push(parseInt(e.substr(n, 2), 16));
        return t
    },
    bytesToBase64: function(e) {
        for (var t = [], r = 0; r < e.length; r += 3)
            for (var o = e[r] << 16 | e[r + 1] << 8 | e[r + 2], i = 0; i < 4; i++)
                8 * r + 6 * i <= 8 * e.length ? t.push(n.charAt(o >>> 6 * (3 - i) & 63)) : t.push("=");
        return t.join("")
    },
    base64ToBytes: function(e) {
        e = e.replace(/[^A-Z0-9+\/]/gi, "");
        for (var t = [], r = 0, o = 0; r < e.length; o = ++r % 4)
            0 != o && t.push((n.indexOf(e.charAt(r - 1)) & Math.pow(2, -2 * o + 8) - 1) << 2 * o | n.indexOf(e.charAt(r)) >>> 6 - 2 * o);
        return t
    }
}

function bytesToString(e) {
    for (var t = [], n = 0; n < e.length; n++)
        t.push(String.fromCharCode(e[n]));
    return t.join("")
}

function xxx(e, t) {
            e.constructor == String ? e = t && "binary" === t.encoding ? a.stringToBytes(e) : o.stringToBytes(e) : i(e) ? e = Array.prototype.slice.call(e, 0) : Array.isArray(e) || (e = e.toString());
            for (var n = r.bytesToWords(e), u = 8 * e.length, c = 1732584193, f = -271733879, l = -1732584194, d = 271733878, p = 0; p < n.length; p++)
                n[p] = 16711935 & (n[p] << 8 | n[p] >>> 24) | 4278255360 & (n[p] << 24 | n[p] >>> 8);
            n[u >>> 5] |= 128 << u % 32,
            n[14 + (u + 64 >>> 9 << 4)] = u;
            var h = s._ff
              , v = s._gg
              , m = s._hh
              , g = s._ii;
            for (p = 0; p < n.length; p += 16) {
                var y = c
                  , w = f
                  , b = l
                  , _ = d;
                f = g(f = g(f = g(f = g(f = m(f = m(f = m(f = m(f = v(f = v(f = v(f = v(f = h(f = h(f = h(f = h(f, l = h(l, d = h(d, c = h(c, f, l, d, n[p + 0], 7, -680876936), f, l, n[p + 1], 12, -389564586), c, f, n[p + 2], 17, 606105819), d, c, n[p + 3], 22, -1044525330), l = h(l, d = h(d, c = h(c, f, l, d, n[p + 4], 7, -176418897), f, l, n[p + 5], 12, 1200080426), c, f, n[p + 6], 17, -1473231341), d, c, n[p + 7], 22, -45705983), l = h(l, d = h(d, c = h(c, f, l, d, n[p + 8], 7, 1770035416), f, l, n[p + 9], 12, -1958414417), c, f, n[p + 10], 17, -42063), d, c, n[p + 11], 22, -1990404162), l = h(l, d = h(d, c = h(c, f, l, d, n[p + 12], 7, 1804603682), f, l, n[p + 13], 12, -40341101), c, f, n[p + 14], 17, -1502002290), d, c, n[p + 15], 22, 1236535329), l = v(l, d = v(d, c = v(c, f, l, d, n[p + 1], 5, -165796510), f, l, n[p + 6], 9, -1069501632), c, f, n[p + 11], 14, 643717713), d, c, n[p + 0], 20, -373897302), l = v(l, d = v(d, c = v(c, f, l, d, n[p + 5], 5, -701558691), f, l, n[p + 10], 9, 38016083), c, f, n[p + 15], 14, -660478335), d, c, n[p + 4], 20, -405537848), l = v(l, d = v(d, c = v(c, f, l, d, n[p + 9], 5, 568446438), f, l, n[p + 14], 9, -1019803690), c, f, n[p + 3], 14, -187363961), d, c, n[p + 8], 20, 1163531501), l = v(l, d = v(d, c = v(c, f, l, d, n[p + 13], 5, -1444681467), f, l, n[p + 2], 9, -51403784), c, f, n[p + 7], 14, 1735328473), d, c, n[p + 12], 20, -1926607734), l = m(l, d = m(d, c = m(c, f, l, d, n[p + 5], 4, -378558), f, l, n[p + 8], 11, -2022574463), c, f, n[p + 11], 16, 1839030562), d, c, n[p + 14], 23, -35309556), l = m(l, d = m(d, c = m(c, f, l, d, n[p + 1], 4, -1530992060), f, l, n[p + 4], 11, 1272893353), c, f, n[p + 7], 16, -155497632), d, c, n[p + 10], 23, -1094730640), l = m(l, d = m(d, c = m(c, f, l, d, n[p + 13], 4, 681279174), f, l, n[p + 0], 11, -358537222), c, f, n[p + 3], 16, -722521979), d, c, n[p + 6], 23, 76029189), l = m(l, d = m(d, c = m(c, f, l, d, n[p + 9], 4, -640364487), f, l, n[p + 12], 11, -421815835), c, f, n[p + 15], 16, 530742520), d, c, n[p + 2], 23, -995338651), l = g(l, d = g(d, c = g(c, f, l, d, n[p + 0], 6, -198630844), f, l, n[p + 7], 10, 1126891415), c, f, n[p + 14], 15, -1416354905), d, c, n[p + 5], 21, -57434055), l = g(l, d = g(d, c = g(c, f, l, d, n[p + 12], 6, 1700485571), f, l, n[p + 3], 10, -1894986606), c, f, n[p + 10], 15, -1051523), d, c, n[p + 1], 21, -2054922799), l = g(l, d = g(d, c = g(c, f, l, d, n[p + 8], 6, 1873313359), f, l, n[p + 15], 10, -30611744), c, f, n[p + 6], 15, -1560198380), d, c, n[p + 13], 21, 1309151649), l = g(l, d = g(d, c = g(c, f, l, d, n[p + 4], 6, -145523070), f, l, n[p + 11], 10, -1120210379), c, f, n[p + 2], 15, 718787259), d, c, n[p + 9], 21, -343485551),
                c = c + y >>> 0,
                f = f + w >>> 0,
                l = l + b >>> 0,
                d = d + _ >>> 0
            }
            return r.endian([c, f, l, d])
        }

function sss(e, t) {
    var n = r.wordsToBytes(xxx(e, t));
    return r.bytesToHex(n)
}

var t
var sign = sss('"/fe_api/burdock/v1/search/note?keyword=%E7%BE%8E%E9%A3%9F&page_size=20WSUDD"', t)