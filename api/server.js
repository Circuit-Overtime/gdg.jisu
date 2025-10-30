const express = require('express');
const path = require('path');
const app = express();

// Import the renderNode function
const { renderNode } = require('../pages/index.js');

// Serve static files
app.use(express.static(path.join(__dirname)));

// Define chapter data
const chapters = {
  gnit: {
    name: 'GNIT',
    gdg_logo: 'https://upload.wikimedia.org/wikipedia/en/c/c1/GNIT_Kolkata_logo.png',
    js_name: 'gnit'
  },
  jisu: {
    name: 'JISU',
    gdg_logo: 'https://www.jisuniversity.ac.in/images/logo.png',
    js_name: 'jisu'
  },
  snu: {
    name: 'SNU',
    gdg_logo: 'https://d299ydywi1tak7.cloudfront.net/media/colleges/28/logo/Sister_Nivedita_University_Logo.png',
    js_name: 'snu'
  },
  tmsl: {
    name: 'TMSL',
    gdg_logo: 'https://media.licdn.com/dms/image/v2/C4D0BAQEZVoTDxFfhfQ/company-logo_200_200/company-logo_200_200/0/1657096672967?e=2147483647&v=beta&t=8c8vLV-IDKVZ436DXIjsaGIBb1LAIKRQ6XZbxn5xG3I',
    js_name: 'tmsl'
  }
};

// Home route
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Dynamic chapter routes
app.get('/:chapter', (req, res) => {
  const chapterKey = req.params.chapter.toLowerCase();
  
  if (chapters[chapterKey]) {
    const { name, gdg_logo, js_name } = chapters[chapterKey];
    const html = renderNode(name, gdg_logo, js_name);
    res.send(html);
  } else {
    res.status(404).send('<h1>Chapter not found</h1>');
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});