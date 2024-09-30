/*
 * @Author: galeliu
 * @Date: 2024-09-25 17:25:47
 * @LastEditTime: 2024-09-27 11:55:34
 * @LastEditors: galeliu
 * @Description: .
 */
// const bip39 = require('bip39');

// let words = bip39.generateMnemonic(256);
// console.log(words);

// console.log('is valid mnemonic? ' + bip39.validateMnemonic(words));

const
    bitcoin = require('bitcoinjs-lib'),
    bip39 = require('bip39');

let
    words = 'bleak version runway tell hour unfold donkey defy digital abuse glide please omit much cement sea sweet tenant demise taste emerge inject cause link',
    password = 'bitcoin';

// 计算seed:
let seedHex = bip39.mnemonicToSeedHex(words, password);
console.log('seed: ' + seedHex); // b59a8078...c9ebfaaa

// 生成root:
let root = bitcoin.HDNode.fromSeedHex(seedHex);
console.log('xprv: ' + root.toBase58()); // xprv9s21ZrQH...uLgyr9kF
console.log('xpub: ' + root.neutered().toBase58()); // xpub661MyMwA...oy32fcRG

// 生成派生key:
let child0 = root.derivePath("m/44'/0'/0'/0/0");
console.log("prv m/44'/0'/0'/0/0: " + child0.keyPair.toWIF()); // KzuPk3PXKdnd6QwLqUCK38PrXoqJfJmACzxTaa6TFKzPJR7H7AFg
console.log("pub m/44'/0'/0'/0/0: " + child0.getAddress()); // 1PwKkrF366RdTuYsS8KWEbGxfP4bikegcS