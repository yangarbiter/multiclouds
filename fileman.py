'''
Created on 2012/12/25

@author: arbiter
'''

html="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>MultiCloud Project</title>
    
    <link type="text/css" rel="stylesheet" href="style/jquery-ui.css" />
    <script type="text/javascript" src="js/jquery-1.8.3.min.js"></script>
    <script type="text/javascript" src="js/used/jquery-ui.js"></script>
    
    <link rel="stylesheet" type="text/css" href="style/data.css" />
    <script type="text/javascript" src="js/json2.js"></script>

    <script type="text/javascript">
    $(document).ready(function () {
        var jsonStr2 = %s
        for( var j=0;j<jsonStr2.length;j++)
        {
            var jsonStr=jsonStr2[j];
            if (jsonStr.total_count) 
            {
                for (var i=0; i<jsonStr.total_count; i++) 
                {
                    LoadBox(jsonStr, i);
                }
            } 
            else if (jsonStr.cloudtype === 'dropbox') 
            {
                for(var i=0; ; i++) 
                {
                    if (!jsonStr.entries[i]) 
                    {
                        break;
                    } 
                    else if (!jsonStr.entries[i][1].is_dir) 
                    {
                        LoadDropbox(jsonStr, i);
                    }
                }
            }
            else 
            {
                for(var i=0; i<jsonStr.items.length; i++) 
                {
                    if (jsonStr.items[i].editable)
                    {
                        LoadGoogleDrive(jsonStr, i);
                    }
                }
                
            }           
        }
    });

    function LoadBox(jsonStr, i) {
        var now = jsonStr.entries[i];
        if ( now.type === 'folder' ) {
            setFolderIcon(now);
        } else if ( now.type === 'file' ) {
            setIcon(now);
        }
    }
    function LoadDropbox(jsonStr, i) {
        var now = jsonStr.entries[i][1];
        if ( now.is_dir ) {
            setFolderIcon2(now);
        } else {
            setIcon2(now);
        }
    }
    function LoadGoogleDrive(jsonStr, i) {
        var now = jsonStr.items[i];
        if ( now.kind === 'drive#parentReference' ) {
            // --
        } else if ( now.kind === 'drive#file' ) {
            setIcon3(now);
        }
    }
    function ReLoadData(now) {
        if (!now.flag) {
            var tmp = now.child;
            for (var f=0; f<tmp.total_count; f++) {
                if ( tmp.entries[f].type === 'folder' ) {
                    setFolderIcon(tmp.entries[f]);
                } else if ( tmp.entries[f].type === 'file' ) {
                    setIcon(tmp.entries[f]); 
                }
            }
            now.flag = true;
        } else {
            alert("Data was already added");
        }
    }
    
    function ShowLink() {
        //
    }
    
    function setFolderIcon(now) {
        // consider file's source cloud and select. >> not used yet
        
        // Random Folder Figure Seed
        var maxNum = 19;  
        var minNum = 0;  
        var n = Math.floor(Math.random() * (maxNum - minNum + 1)) + minNum;
        // End Seed
        var img = document.createElement("img");
        img.src = 'icon/folder/' + n + '.ico';
        var t = document.createElement("div");
        var t2 = document.createElement("div");
        var t3 = document.createElement("div");
        t.className = 'portlet';
        t2.className = 'portlet-header';
        t3.className = 'portlet-content';
        t3.addEventListener('dblclick', function() {
            //$(".portlet").style = "display: none";
            ReLoadData(now);
        }, false);
            //
            //
            //$("img").on("click", "img", function() {
            //$(this).toggleClass("chosen");
            //});
        t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
        t3.addEventListener('mouseover', function() {
            this.style.cursor = 'hand';
        }, false);
        t3.appendChild(img);
        t.appendChild(t2);
        t.appendChild(t3);
        $(".column")[0].appendChild(t);
    }
    
    function setFolderIcon2(now) {
        // Random Folder Figure Seed
        var maxNum = 19;  
        var minNum = 0;  
        var n = Math.floor(Math.random() * (maxNum - minNum + 1)) + minNum;
        // End Seed
        var img = document.createElement("img");
        img.src = 'icon/folder/' + n + '.ico';
        var t = document.createElement("div");
        var t2 = document.createElement("div");
        var t3 = document.createElement("div");
        t.className = 'portlet';
        t2.className = 'portlet-header';
        t3.className = 'portlet-content';
        t3.addEventListener('dblclick', function() {
            //$(".portlet").style = "display: none";
            ReLoadData(now);
        }, false);
        t2.appendChild(document.createTextNode( now.path.substr(-9) ));
        t3.addEventListener('mouseover', function() {
            this.style.cursor = 'hand';
        }, false);
        t3.appendChild(img);
        t.appendChild(t2);
        t.appendChild(t3);
        $(".column")[1].appendChild(t);
    }

    function setIcon(now) {

        if ( now.name.match(/.txt$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/txt.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[0].appendChild(t);
        } else if ( now.name.match(/.bat$/) || now.name.match(/.cmd$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/bat.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[0].appendChild(t);
        } else if ( now.name.match(/.cpp$/) || now.name.match(/.c$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/cpp.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[0].appendChild(t);
        } else if ( now.name.match(/.doc$/) || now.name.match(/.docx$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/doc.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[0].appendChild(t);
        } else if ( now.name.match(/.exe$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/exe.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[1].appendChild(t);
        } else if ( now.name.match(/.htm$/) || now.name.match(/.html$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/html.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[1].appendChild(t);
        } else if ( now.name.match(/.java$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/java.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[1].appendChild(t);
        } else if ( now.name.match(/.js$/) || now.name.match(/.json$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/js.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[1].appendChild(t);
        } else if ( now.name.match(/.css$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/css.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[2].appendChild(t);
        } else if ( now.name.match(/.mp3$/) || now.name.match(/.wav$/) || now.name.match(/.midi$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/Music.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[2].appendChild(t);
        } else if ( now.name.match(/.pdf$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/pdf.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[2].appendChild(t);
        } else if ( now.name.match(/.jpg$/) || now.name.match(/.jpeg$/) || now.name.match(/.png$/) || now.name.match(/.bmp$/) || now.name.match(/.gif$/) || now.name.match(/.ico$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/pic.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[2].appendChild(t);
        } else if ( now.name.match(/.ppt$/) || now.name.match(/.pptx$/) || now.name.match(/.pps$/) || now.name.match(/.ppsx$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/ppt.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[3].appendChild(t);
        } else if ( now.name.match(/.pub$/) || now.name.match(/.pubx$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/pub.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[3].appendChild(t);
        } else if ( now.name.match(/.rar$/) || now.name.match(/.7z$/) || now.name.match(/.tar$/) || now.name.match(/.zip$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/rar.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[3].appendChild(t);
        } else if ( now.name.match(/.sql$/) || now.name.match(/.dat$/) || now.name.match(/.sys$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/sql.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[3].appendChild(t);
        } else if ( now.name.match(/.torrent$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/torrent.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[4].appendChild(t);
        } else if ( now.name.match(/.mp4$/) || now.name.match(/.rmvb$/) || now.name.match(/.rm$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/Video.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[4].appendChild(t);
        } else if ( now.name.match(/.wmv$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/wmv.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[4].appendChild(t);
        } else if ( now.name.match(/.xls$/) || now.name.match(/.xlsx$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/xls.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[4].appendChild(t);
        } else {
            var img = document.createElement("img");
            img.src = 'icon/others.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.name.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[4].appendChild(t);
        }
    }
    
    function setIcon2(now) {
        if ( now.path.match(/.txt$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/txt.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[0].appendChild(t);
        } else if ( now.path.match(/.bat$/) || now.path.match(/.cmd$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/bat.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[0].appendChild(t);
        } else if ( now.path.match(/.cpp$/) || now.path.match(/.c$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/cpp.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[0].appendChild(t);
        } else if ( now.path.match(/.doc$/) || now.path.match(/.docx$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/doc.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[0].appendChild(t);
        } else if ( now.path.match(/.exe$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/exe.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[1].appendChild(t);
        } else if ( now.path.match(/.htm$/) || now.path.match(/.html$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/html.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[1].appendChild(t);
        } else if ( now.path.match(/.java$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/java.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[1].appendChild(t);
        } else if ( now.path.match(/.js$/) || now.path.match(/.json$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/js.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[1].appendChild(t);
        } else if ( now.path.match(/.css$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/css.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[2].appendChild(t);
        } else if ( now.path.match(/.mp3$/) || now.path.match(/.wav$/) || now.path.match(/.midi$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/Music.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[2].appendChild(t);
        } else if ( now.path.match(/.pdf$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/pdf.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[2].appendChild(t);
        } else if ( now.path.match(/.jpg$/) || now.path.match(/.jpeg$/) || now.path.match(/.png$/) || now.path.match(/.bmp$/) || now.path.match(/.gif$/) || now.path.match(/.ico$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/pic.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[2].appendChild(t);
        } else if ( now.path.match(/.ppt$/) || now.path.match(/.pptx$/) || now.path.match(/.pps$/) || now.path.match(/.ppsx$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/ppt.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[3].appendChild(t);
        } else if ( now.path.match(/.pub$/) || now.path.match(/.pubx$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/pub.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[3].appendChild(t);
        } else if ( now.path.match(/.rar$/) || now.path.match(/.7z$/) || now.path.match(/.tar$/) || now.path.match(/.zip$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/rar.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[3].appendChild(t);
        } else if ( now.path.match(/.sql$/) || now.path.match(/.dat$/) || now.path.match(/.sys$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/sql.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[3].appendChild(t);
        } else if ( now.path.match(/.torrent$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/torrent.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[4].appendChild(t);
        } else if ( now.path.match(/.mp4$/) || now.path.match(/.rmvb$/) || now.path.match(/.rm$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/Video.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[4].appendChild(t);
        } else if ( now.path.match(/.wmv$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/wmv.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[4].appendChild(t);
        } else if ( now.path.match(/.xls$/) || now.path.match(/.xlsx$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/xls.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[4].appendChild(t);
        } else {
            var img = document.createElement("img");
            img.src = 'icon/others.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.path.substr(-9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[4].appendChild(t);
        }
    }
    
    function setIcon3(now) {
    
        if ( now.title.match(/.txt$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/txt.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[0].appendChild(t);
        } else if ( now.title.match(/.bat$/) || now.title.match(/.cmd$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/bat.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[0].appendChild(t);
        } else if ( now.title.match(/.cpp$/) || now.title.match(/.c$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/cpp.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[0].appendChild(t);
        } else if ( now.title.match(/.doc$/) || now.title.match(/.docx$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/doc.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[0].appendChild(t);
        } else if ( now.title.match(/.exe$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/exe.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[1].appendChild(t);
        } else if ( now.title.match(/.htm$/) || now.title.match(/.html$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/html.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[1].appendChild(t);
        } else if ( now.title.match(/.java$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/java.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[1].appendChild(t);
        } else if ( now.title.match(/.js$/) || now.title.match(/.json$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/js.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[1].appendChild(t);
        } else if ( now.title.match(/.css$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/css.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[2].appendChild(t);
        } else if ( now.title.match(/.mp3$/) || now.title.match(/.wav$/) || now.title.match(/.midi$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/Music.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[2].appendChild(t);
        } else if ( now.title.match(/.pdf$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/pdf.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[2].appendChild(t);
        } else if ( now.title.match(/.jpg$/) || now.title.match(/.jpeg$/) || now.title.match(/.png$/) || now.title.match(/.bmp$/) || now.title.match(/.gif$/) || now.title.match(/.ico$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/pic.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[2].appendChild(t);
        } else if ( now.title.match(/.ppt$/) || now.title.match(/.pptx$/) || now.title.match(/.pps$/) || now.title.match(/.ppsx$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/ppt.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[3].appendChild(t);
        } else if ( now.title.match(/.pub$/) || now.title.match(/.pubx$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/pub.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[3].appendChild(t);
        } else if ( now.title.match(/.rar$/) || now.title.match(/.7z$/) || now.title.match(/.tar$/) || now.title.match(/.zip$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/rar.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[3].appendChild(t);
        } else if ( now.title.match(/.sql$/) || now.title.match(/.dat$/) || now.title.match(/.sys$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/sql.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[3].appendChild(t);
        } else if ( now.title.match(/.torrent$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/torrent.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[4].appendChild(t);
        } else if ( now.title.match(/.mp4$/) || now.title.match(/.rmvb$/) || now.title.match(/.rm$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/Video.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[4].appendChild(t);
        } else if ( now.title.match(/.wmv$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/wmv.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[4].appendChild(t);
        } else if ( now.title.match(/.xls$/) || now.title.match(/.xlsx$/) ) {
            var img = document.createElement("img");
            img.src = 'icon/xls.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[4].appendChild(t);
        } else {
            var img = document.createElement("img");
            img.src = 'icon/others.ico';
            var t = document.createElement("div");
            var t2 = document.createElement("div");
            var t3 = document.createElement("div");
            t.className = 'portlet';
            t2.className = 'portlet-header';
            t3.className = 'portlet-content';
            t2.appendChild(document.createTextNode( now.title.substring(0, 9) ));
            // // t3.addEventListener('click', ReLoadData(now), false);
            t3.appendChild(img);
            t.appendChild(t2);
            t.appendChild(t3);
            $(".column")[4].appendChild(t);
        }
    }
    </script>
<!--
<div id="ConentDiv">
    <input type="button" id ="Button2" value="new"/>
    <input type="hidden" id="Count" name="Count" value="2" />
    </div>
    <div id="TextValueDiv"> 
     <input type="text" id="text1" name="text1" /><br />   
</div> 
-->
    <script> // 
        function cleanup() {
            jQuery.each( function() {
                $('.column').html('');
            });
        }
    </script>
    
    <style>
        .column {
            width: 130px;
            float: left;
            padding-bottom: 100px;
            margin: 15px;
        }
        .column img {
            width: 100px; 
            height: 75px;
        }
        .portlet {
            margin: 0 1em 1em 0;
            background: transparent;
        }
        .portlet-header {
            font-weight: normal;
            font-size: 10px;
            margin: 0.3em;
            padding-bottom: 4px;
            padding-left: 0.2em;
        }
        .portlet-header .ui-icon {
            float: right;
        }
        .portlet-content {}
        .ui-sortable-placeholder {
            border: 1px solid skyblue;
            visibility: visible !important;
            height: 100px !important;
        }
        .ui-sortable-placeholder * {
            visibility: hidden;
        }
    </style>
    <script>
        $(function() {
            $( ".column" ).sortable({
                connectWith: ".column"
            });
     
            $( ".portlet" ).addClass( "ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" )
                .find( ".portlet-header" )
                    .addClass( "ui-widget-header ui-corner-all" )
                    .prepend( "<span class='ui-icon ui-icon-minusthick'></span>")
                    .end()
                .find( ".portlet-content" );
     
            $( ".portlet-header .ui-icon" ).click(function() {
                $( this ).toggleClass( "ui-icon-minusthick" ).toggleClass( "ui-icon-plusthick" );
                $( this ).parents( ".portlet:first" ).find( ".portlet-content" ).toggle();
            });
     
            $( ".column" ).disableSelection();
        });
    </script>

</head>
    <body>
        <div id="main">
            <div id="head">
                <h1>MultiCloud</h1>
                <h2>File Management</h2>
            </div>

            <div id="menu">
                <a href="http://multiclouds.appspot.com/user">&nbsp&nbspHome&nbsp&nbsp&nbsp </a>
                <a href="http://multiclouds.appspot.com/user/contactus">&nbspContact&nbsp</a>
            </div>

            <div id="content">
                <div class="column">
                </div>
                 
                <div class="column"> 
                </div>
                 
                <div class="column">
                 

                 
                </div>
                
                <div class="column">
                </div>
                
                <div class="column"> 
                </div>

            </div>

        </div>

        <div id="foot">
        
        </div>
        
    
    </body>
</html>
"""
def get(string):
    return html%string