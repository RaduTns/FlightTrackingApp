    
    var orig = origVar;
    var dest = destVar;
    const origLabel = new Array();
    const origData = new Array();
    const destLabel = new Array();
    const destData = new Array();
    for(let i = 0; i < orig.length; i++)
    {
        origLabel.push(orig[i].airport)
        origData.push(orig[i].tracked_flights)
    }
    for(let i = 0; i < orig.length; i++)
    {
        destLabel.push(dest[i].airport)
        destData.push(dest[i].tracked_flights)
    }
    const dataOrig = {
        labels: origLabel,
        datasets: [{
            data:origData,
            fill: true,
            backgroundColor: ['rgb(131, 174, 242)','rgb(54, 162, 235)','rgb(255, 205, 86)'],
            tension: 0.1,

        }]
    }
    const dataDest = {
        labels: destLabel,
        datasets: [{
            data:destData,
            fill: true,
            backgroundColor: ['rgb(131, 174, 242)','rgb(255, 99, 132)','rgb(54, 162, 235)','rgb(255, 205, 86)'],
            tension: 0.1,

        }]
    }
    const configOrig = {
    type: 'pie',
    data: dataOrig,
    };

    const configDest = {
    type: 'pie',
    data: dataDest,
    };

    const chartOrig = new Chart(
        document.getElementById('myChartOrig'),
        configOrig
    )
    const chartDest = new Chart(
        document.getElementById('myChartDest'),
        configDest
    )