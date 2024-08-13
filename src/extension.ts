import * as vscode from 'vscode';
// import {getHtmlContent} from './webview';

//TODO: add shortcuts later.
export function activate(context: vscode.ExtensionContext) {
	let stackOverdlowView = vscode.commands.registerCommand('trackoverflow.extension.soView',() => {

		const panel = vscode.window.createWebviewPanel(
			'stackOverflow',
			'StackOverflow View',
			vscode.ViewColumn.Two,
			{
				enableScripts: true, 
			}
		);	

        // Get path to resource on disk
        const scriptPath = vscode.Uri.joinPath(context.extensionUri, 'src/js', 'so.js');
        const cssPagth = vscode.Uri.joinPath(context.extensionUri, 'src/css', 'style.css');
        
        // And get the special URI to use with the webview
        const scriptSrc = panel.webview.asWebviewUri(scriptPath);
        const cssSrc = panel.webview.asWebviewUri(cssPagth);

		panel.webview.html = getHtmlContent(scriptSrc, cssSrc);


        //handle message from webview.
        panel.webview.onDidReceiveMessage(
            message => {
                switch(message.command){
                    case 'codeCopied':
                        vscode.window.showInformationMessage(message.text);
                        return;
                }
            }, 
            undefined, 
            context.subscriptions
        );
	});
	context.subscriptions.push(stackOverdlowView);
}

// this method is called when your extension is deactivated
export function deactivate() {}


function getHtmlContent(scriptSrc: vscode.Uri, cssSrc: vscode.Uri) {
return  `
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Integrated Stackoverflow Search</title>
        <link href="https://fonts.googleapis.com/css?family=Roboto+Condensed&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="${cssSrc}">
        <link rel="shortcut icon" href="logo-192.png" type="image/x-icon">
        <style>
            body{
                background-color:#ddd !important;
            }
        </style>
    </head>
    <body>
        <div style="padding:20px;">
            <label for="search" style="color:#111;font-weight:bold;">Search</label>
            <div style="display:flex;">
                <input id="search" style="display:inline-block;width:75%;padding:6px;flex:1;" type="search">
                <button class="search-button blue-button">Search</button>
            </div>
            <div id="answers" style="margin-top:20px;">
            </div>
        </div>
        <script src="${scriptSrc}"></script>
    </body>
</html>
`;
}
