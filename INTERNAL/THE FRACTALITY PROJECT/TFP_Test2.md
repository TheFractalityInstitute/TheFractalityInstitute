<!DOCTYPE html>
<html lang="en">
<head>
    <title>OrbitControls Test</title>
    <script type="importmap">
    {
      "imports": {
        "../../../build/three.module.js": "./three.module.js"
      }
    }
    </script>
    <style>
      body { background: #333; color: white; font-family: sans-serif; font-size: 1.5em; text-align: center; padding: 10%; }
      #success { color: #7CFC00; }
      #fail { color: #FF6347; font-weight: bold; }
      small { color: #aaa; font-size: 0.7em; }
    </style>
</head>
<body>
    <h1>OrbitControls Load Test</h1>
    <p id="message">Attempting to load OrbitControls.js...</p>
    <script type="module">
        try {
            // We are only importing OrbitControls. The browser should
            // see that it needs three.module.js and load it automatically.
            await import('./OrbitControls.js');
            document.getElementById('message').innerHTML = '<span id="success">SUCCESS! OrbitControls.js and its dependency were loaded.</span>';
        } catch (error) {
            document.getElementById('message').innerHTML = '<span id="fail">FAILURE! OrbitControls.js could not be loaded.</span><br><br><small>' + error + '</small>';
        }
    </script>
</body>
</html>
