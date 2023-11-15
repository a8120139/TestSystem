// 必要なモジュールのインポート
const express = require('express');
const mongoose = require('mongoose');

// Expressアプリの初期化
const app = express();

// MongoDBへの接続
mongoose.connect('mongodb://localhost/barbershop', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

// MongoDBのスキーマ定義（例）
const shopSchema = new mongoose.Schema({
    name: String,
    openingHours: {
        type: String,
        default: '09:00 - 18:00', // デフォルトの営業時間
    },
    waitingTime: {
        type: Number,
        default: 0, // デフォルトの待ち時間
    },
});

// MongoDBモデルの作成
const Shop = mongoose.model('Shop', shopSchema);

// GETリクエストに対するエンドポイントの作成（例）
app.get('/api/shop/:id', async (req, res) => {
    try {
        const shop = await Shop.findById(req.params.id);
        res.json(shop);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// POSTリクエストに対するエンドポイントの作成（例）
app.post('/api/shop', async (req, res) => {
    const shop = new Shop({
        name: req.body.name,
        openingHours: req.body.openingHours,
        waitingTime: req.body.waitingTime,
    });

    try {
        const newShop = await shop.save();
        res.status(201).json(newShop);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
});

// サーバーの起動
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server started on port ${PORT}`);
});
