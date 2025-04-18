/**
 * @license Copyright (c) 2003-2016, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) 
{
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	
	//開啟圖片上傳功能 
	config.filebrowserBrowseUrl = 'ckfinder_2.6.0/ckfinder.html';
	config.filebrowserImageBrowseUrl = 'ckfinder_2.6.0/ckfinder.html?Type=Images';
	config.filebrowserFlashBrowseUrl = 'ckfinder_2.6.0/ckfinder.html?Type=Flash';
	config.filebrowserUploadUrl = 'ckfinder_2.6.0/core/connector/php/connector.php?command=QuickUpload&type=Files'; //可上傳一般檔案
	config.filebrowserImageUploadUrl = 'ckfinder_2.6.0/core/connector/php/connector.php?command=QuickUpload&type=Images';//可上傳圖檔
};
