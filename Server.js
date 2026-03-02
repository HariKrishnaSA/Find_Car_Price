const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const app = express();


app.use(express.json());

app.use(express.static('public'));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'Frontend.html'));
});

app.post('/predict', (req, res) => {
    
    const { brand, model, year, km, fuel, seller, trans, owner } = req.body;

    /** * 2. Execute Python script (predict.py)
     * We check the platform: 'python' for Windows, 'python3' for Linux (Cloud)
     */
    const pythonCmd = process.platform === "win32" ? "python" : "python3";

    const py = spawn(pythonCmd, [
        'Predict.py', 
        brand, 
        model, 
        year, 
        km, 
        fuel, 
        seller, 
        trans, 
        owner
    ]);

    let result = "";
    let errorOutput = "";


    py.stdout.on('data', (data) => {
        result += data.toString();
    });


    py.stderr.on('data', (data) => {
        errorOutput += data.toString();
        console.error(`Python Logic Error: ${data}`);
    });


    py.on('close', (code) => {
        if (code !== 0) {
            console.error(`Exit Code: ${code}, Error: ${errorOutput}`);
            return res.status(500).json({ error: "Prediction failed" });
        }

        res.json({ price: result.trim() });
    });
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`===========================================`);
    console.log(`CAR PRICE FIND ACTIVATED`);
    console.log(`PORT: ${PORT}`);
    console.log(`Status: Version 2.0 (Model-Aware)`);
    console.log(`===========================================`);
});