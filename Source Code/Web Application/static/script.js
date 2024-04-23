const firebaseConfig = {
    apiKey: "AIzaSyBnZOE9F23_750lxMV6S5tz_axfArMh6FI",
    authDomain: "test-firebase-4d32f.firebaseapp.com",
    databaseURL: "https://test-firebase-4d32f-default-rtdb.firebaseio.com",
    projectId: "test-firebase-4d32f",
    storageBucket: "test-firebase-4d32f.appspot.com",
    messagingSenderId: "376881877023",
    appId: "1:376881877023:web:73ccc6c0c902e06760452a",
    measurementId: "G-F95EC0DEJS"
};

firebase.initializeApp(firebaseConfig);

var database = firebase.database();
var dataRef = database.ref();

const time = document.getElementById('time')

function fetchDataAndHtmlUpdate() {
    fetchData().then(data => updateHTML(data));
}

function fetchData() {
    return fetch("/predict")
        .then(response => response.json())
        .then(data => {
            console.log(data);
            return data;
        });
}

function updateHTML(data) {
    time.innerHTML = `Update lastest : ${data.Timestamp}`;
    let color;
    for (let i = 1; i <= 8; i++) {
        let gridValue = data[`Grid9to${i}`];
        let gridRef = data.GridRef;

        if (gridValue > 40 || gridRef > 40) {
            color = '#420C09';
        } else if ((gridValue >= 33 && gridValue < 39) || (gridRef >= 33 && gridRef < 39)) {
            color = '#FF0000';
        } else if ((gridValue >= 27 && gridValue < 32) || (gridRef >= 27 && gridRef < 32)) {
            color = '#f7e334';
        } else if ((gridValue >= 22 && gridValue < 26) || (gridRef >= 22 && gridRef < 27)) {
            color = '#32CD32';
        } else if (gridValue < 22 || gridRef < 22) {
            color = '#87CEEB';
        }



        if (`G${i}` >= `G${1}` && `G${i}` <= `G${9}`) {
            console.log(`<h1 style="background-color: ${color};">Grid9to${i}, ${data[`Grid9to${i}`]}</h1>`);
            document.getElementById(`G${i}`).innerHTML = `<h1 style="background-color: ${color}; padding: 20px; text-align: center; border-radius: 5px;">${gridValue}</h1>`;
            if (gridRef === data.GridRef) {
                document.getElementById("G9").innerHTML = `<h1 style="background-color: ${color}; padding: 20px; text-align: center; border-radius: 5px;">${gridRef}</h1>`;
            }
        }
    }
}

dataRef.on('value', (snapshot) => {
    fetchDataAndHtmlUpdate();
});









// try {
//     var xValues = ['G3', 'G6', 'G9'];
//     var yValues = ['G1', 'G2', 'G3'];
//     var zValues = [
//         [data.GridRef, data.Grid1to4, data.Grid1to7],
//         [data.Grid1to2, data.Grid1to5, data.Grid1to8],
//         [data.Grid1to3, data.Grid1to6, data.Grid1to9]
//     ];

//     var heatmapData = [{
//         x: xValues,
//         y: yValues,
//         z: zValues,
//         type: 'heatmap',
//         showscale: true,
//         colorscale: colorscale
//     }];

//     var layout = {
//         // title: 'Heatmap',
//         font: {
//             family: 'kanit',
//             size: 25,
//         },
//         annotations: [],
//         xaxis: {
//             ticks: '',
//             side: 'top'
//         },
//         yaxis: {
//             ticks: '',
//             side: 'left',
//             automargin: false
//         },
//         width: 1000,
//         height: 600
//     };

//     for (var i = 0; i < yValues.length; i++) {
//         for (var j = 0; j < xValues.length; j++) {
//             var result = {
//                 xref: 'x1',
//                 yref: 'y1',
//                 x: xValues[j],
//                 y: yValues[i],
//                 text: zValues[i][j],
//                 font: {
//                     family: 'kanit',
//                     size: 25,
//                     color: '#ffffff'
//                 },
//                 showarrow: false,
//             };
//             layout.annotations.push(result);
//         }
//     }

//     // ตรวจสอบที่มีการเรียก Plotly.newPlot ในที่ถูกต้อง
//     Plotly.newPlot('test', heatmapData, layout);

// } catch (error) {
//     console.error('Error updating HTML:', error);
// }



// fetchData();
// setInterval(fetchData, 300000);
// setInterval(fetchData, 5000);
