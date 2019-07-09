import json

table_content = "tr = tr + "

with open('test.json') as json_file:  
    data = json.load(json_file)
    rowBlock = ""
    for x in data:
       rowBlock += '\'<tr>\'' + ' + ' + '\'<td>\'' + ' + ' + '\'' + x + '\'' + ' + ' + '\'</td>\'' + ' + ' + '\'<td>\'' + ' + ' + '\'' + data[x]['name'] + '\'' + ' + ' + '\'</td>\'' + ' + ' + '\'<td>\'' + ' + ' + '\'' + data[x]['discount'] + '\'' + ' + ' + '\'</td>\'' + ' + ' + '\'</tr>\'' + '+'
       print(data[x]['name'])
       print(data[x]['discount'])
    rowBlock = rowBlock[:-1]
    table_content += rowBlock + ';'

#table_content = "tr = tr + '<tr>' + '<td>' + '7776' + '</td>' + '<td>' + 'NieR:Automata™' + '</td>' + '<td>' + '50' + '</td>' + '</tr>' + '<tr>' + '<td>' + '1234' + '</td>' + '<td>' + 'GameTitle' + '</td>' + '<td' + '65' + '</td>' + '</tr>'";

#template = """1st header line
#second header line
#There are {npeople:5.2f} people in {nrooms} rooms
#and the {ratio} is {large}
#""" 
#context = {
# "npeople":npeople, 
# "nrooms":nrooms,
# "ratio": ratio,
# "large" : large
# } 
#with  open('out.txt','w') as myfile:
#    myfile.write(template.format(**context))

template = """<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
{{
  box-sizing: border-box;
}}

#myInput {{
  background-image: url('/css/searchicon.png');
  background-position: 10px 10px;
  background-repeat: no-repeat;
  width: 100%;
  font-size: 16px;
  padding: 12px 20px 12px 40px;
  border: 1px solid #ddd;
  margin-bottom: 12px;
}}

#myTable {{
  border-collapse: collapse;
  width: 100%;
  border: 1px solid #ddd;
  font-size: 18px;
}}

#myTable th, #myTable td {{
  text-align: left;
  padding: 12px;
}}

#myTable tr {{
  border-bottom: 1px solid #ddd;
}}

#myTable tr.header, #myTable tr:hover {{
  background-color: #e8d7f2;
}}
</style>
</head>
<body background="skulls.png" onload="wrapperFunc();">

<h1 align="center" style="font-family:arial">Welcome to Steam Buddy!</h1>
<h2 style="font-family:arial">Use the boxes below to search for sales data!</h2>

<input type="text" id="myInputGame" onkeyup="filterByGame()" placeholder="Search for games.." title="Type in a name">
<input type="text" id="myInputAPPID" onkeyup="filterByAPPID()" placeholder="Search by APPID.." title="Type in a name">
<input type="text" id="myInputDiscount" onkeyup="filterByDiscount()" placeholder="Search for Discount.." title="Type in a name">

<div id="test" align="center" style="font-family:arial"></div>

<p style="font-family:arial"> This is just a BETA page. Copyright TinyFlameRob.co.uk. Don't webcrawl me bro! </p>

<script>

function buildTable() {{
    var tr = '<table id="myTable" style="width":100% border="1">';
    //tr = tr + '<tr>';
    tr = tr + '<th>' + 'AppID' + '</th>' + '<th>' + 'Title Name' + '</th>' + '<th>' +  'Discount %' + '</th>' + '<th>' + 'Sale Price' + '</th>' + '<th>' + 'Full Price' + '</th>';

    {table_content}
    tr = tr + '</table>'
    return tr;
}}

function filterByGame() {{
  var input, filter, table, tr, td, i;
  input = document.getElementById("myInputGame");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++){{
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {{
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {{
        tr[i].style.display = "";
      }} else {{
        tr[i].style.display = "none";
      }}
    }}
  }}
}}

function filterByAPPID() {{
  var input, filter, table, tr, td, i;
  input = document.getElementById("myInputAPPID");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {{
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {{
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {{
        tr[i].style.display = "";
      }} else {{
        tr[i].style.display = "none";
      }}
    }}
  }}
}}

function filterByDiscount() {{
  var input, filter, table, tr, td, i;
  input = document.getElementById("myInputDiscount");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {{
    td = tr[i].getElementsByTagName("td")[2];
    if (td) {{
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {{
        tr[i].style.display = "";
      }} else {{
        tr[i].style.display = "none";
      }}
    }}
  }}
}}

function wrapperFunc()
{{
        var endVar = buildTable();
        console.log("endVar: " + endVar);
        document.getElementById("test").innerHTML = endVar;
}}

</script>

</body>
</html>"""
context = {
 "table_content":table_content,
}
with  open('index.html','w') as myfile:
    myfile.write(template.format(**context))

