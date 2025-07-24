<!DOCTYPE html>
<html lang="en">
<head>
    <title>Module Test</title>
    <style>
      body { background: #333; color: white; font-family: sans-serif; font-size: 2em; text-align: center; padding-top: 20%; }
      #success { color: #7CFC00; }
      #fail { color: #FF6347; }
    </style>
</head>
<body>
    <h1>Module Load Test</h1>
    <p id="message">Attempting to load script...</p>

    <script type="module">
        // The only goal of this script is to import a file.
        // If this works, the message on the screen will change.
        try {
            await import('./three.module.js');
            document.getElementById('message').innerHTML = '<span id="success">SUCCESS! The server can load JavaScript modules.</span>';
        } catch (error) {
            document.getElementById('message').innerHTML = '<span id="fail">FAILURE! The server cannot load JavaScript modules.</span><br><small>' + error + '</small>';
        }
    </script>
</body>
</html>
