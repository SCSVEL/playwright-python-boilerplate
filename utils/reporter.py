import base64
from datetime import datetime
from os import environ


class Reporter:
    def __init__(self, title, page):
        self.title = title
        self.output_file = "../reports/" + title + ".html"
        self.page = page
        self.steps = []

    def _take_screenshot(self):
        screenshot_path = environ.get("TMP") + "/screenshot.png"
        self.page.screenshot(path=screenshot_path)
        return screenshot_path

    def report_pass(self, step_description: str):
        self._add_step(step_description, "PASS", self._take_screenshot())

    def report_fail(self, step_description: str):
        self._add_step(step_description, "FAIL", self._take_screenshot())

    def report_warn(self, step_description: str):
        self._add_step(step_description, "WARN", self._take_screenshot())

    def report_info(self, step_description: str):
        self._add_step(step_description, "INFO")


    def _add_step(self, desc, status, screenshot_path=None):
        self.steps.append({
            "desc": desc,
            "status": status,
            "time": datetime.now().strftime("%H:%M:%S"),
            "screenshot_path": screenshot_path
        })

    def _encode_image_to_base64(self, path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def _generate_html(self):
        html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>{self.title}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        text-align: center;
                    }}
                    table {{
                        margin: auto;
                        border-collapse: collapse;
                        width: auto;
                        table-layout: auto;
                    }}
                    th, td {{
                        border: 1px solid #ccc;
                        padding: 10px;
                        width: fit-content;                        
                    }}
                    th {{
                        background-color: #f2f2f2;
                    }}                    
                    td.desc {{
                        text-align: left;
                    }}
                    .dialog-overlay {{
                        position: fixed;
                        top: 0; left: 0;
                        width: 100%; height: 100%;
                        background: rgba(0,0,0,0.5);
                        display: none;
                        justify-content: center;
                        align-items: center;
                    }}
                    .dialog-box {{
                        background: white;
                        padding: 20px;
                        border-radius: 8px;
                        max-width: 80%;
                    }}
                    .popup-img img {{
                        max-width: 100%;
                        max-height: 80%;
                    }}
                    .close-btn {{
                        margin-top: 10px;
                        cursor: pointer;
                        color: #007BFF;
                    }}
                </style>
            </head>
            <body>
                <h2>{self.title}</h2>
                <table>
                    <tr>
                        <th>S.No</th>
                        <th>Step Description</th>
                        <th>Status</th>
                        <th>Time</th>
                    </tr>
            """

        for i, step in enumerate(self.steps, start=1):
            if step["status"].upper() == "PASS":
                sts_style = "style=\"color:green;"
            elif step["status"].upper() == "FAIL":
                sts_style = "style=\"color:red;"
            elif step["status"].upper() == "WARN":
                sts_style = "style=\"color:yellow;"
            elif step["status"].upper() == "INFO":
                sts_style = "style=\"color:blue;"
            else:
                sts_style = "\""

            if step["screenshot_path"]:
                img_base64 = self._encode_image_to_base64(step["screenshot_path"])
                td_sts = f"""<td {sts_style}text-decoration: underline;cursor: pointer;" onclick="showDialog( 
                    '{img_base64}')">{step["status"]}</td>"""
            else:
                td_sts = f"""<td {sts_style}">{step["status"]}</td>"""

            html += f"""
                <tr>
                    <td>{i}</td>
                    <td class="desc">{step["desc"]}</td> 
                    {td_sts}
                    <td>{step["time"]}</td>
                </tr> """

        html += """
            </table>            
            <div class="dialog-overlay" id="dialog">
                <div class="dialog-box">
                <div class="close-btn" onclick="closeDialog()">Close</div>                    
                    <div class="popup-img">
                        <img id="screenshotImg" src="" alt="Screenshot" />
                    </div>                    
                </div>
            </div>
        
            <script>
                function showDialog(base64Img) {                    
                    document.getElementById('screenshotImg').src = 'data:image/png;base64,' + base64Img;
                    document.getElementById('dialog').style.display = 'flex';
                }
        
                function closeDialog() {
                    document.getElementById('dialog').style.display = 'none';
                }
            </script>
        </body>
        </html> """

        return html

    def save(self):
        with open(self.output_file, "w") as file:
            file.write(self._generate_html())
        print(f"✅ HTML report saved as: {self.output_file}")
