const express = require("express");
const multer = require("multer");
const app = express();
const port = 3000;

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "./uploads");
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  },
});

var upload = multer({ storage: storage });

// auto create folder uploads
const fs = require("fs");
const dir = "./uploads";
if (!fs.existsSync(dir)) {
  fs.mkdirSync(dir);
}

//multer middleware
app.use(multer({ storage }).single("file"));  


app.get("/download/:filename", (req, res) => {
  const { filename } = req.params;
  res.download(`./uploads/${filename}`);
});

//handler post to upload file using multer middleware
app.post("/upload", upload.single("file"), (req, res) => {
  const file = req.file
  console.log(file);
  if (!file) {
    const error = new Error('Please upload a file')
    error.httpStatusCode = 400
    res.send(error);
    return;
  }
    res.send(res.status(200).json({ message: "File uploaded successfully" }));
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});