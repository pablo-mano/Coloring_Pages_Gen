const { spawn } = require('child_process');
const path = require('path');

/**
 * Calls the Python coloring book generator script with the given theme and count.
 * Returns a Promise that resolves to the output directory and filenames.
 */
function generateColoringPages(theme, count = 1) {
  return new Promise((resolve, reject) => {
    const scriptPath = path.resolve(__dirname, '../generate_coloring_book.py');
    const args = ['-t', theme, '-n', String(count)];
    const pythonProcess = spawn('python', [scriptPath, ...args], { encoding: 'utf-8' });

    let stdout = '';
    let stderr = '';

    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });
    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    pythonProcess.on('close', (code) => {
      if (code === 0) {
        // Try to extract the output folder from stdout
        const match = stdout.match(/Output folder: (.*)/);
        const outputDir = match ? match[1].trim() : null;
        resolve({ stdout, outputDir });
      } else {
        reject(new Error(`Script exited with code ${code}: ${stderr}`));
      }
    });
  });
}

module.exports = { generateColoringPages };
