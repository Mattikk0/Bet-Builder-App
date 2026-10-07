function prepareJSON(){
	const selectedRisk = lowRisk.checked
		? 0.125
		: normalRisk.checked
			? 0.250
			: highRisk.checked
				? 0.5
				: null;

	const leagues = Array.from(
		document.querySelectorAll("#league-container input[type='checkbox']:checked")
	).map(checkbox => checkbox.labels[0].textContent.trim());

	return {
		targetAKO: Number((akoSlider.value / 10).toFixed(1)),
		games: Number(gamesSlider.value),
		risk: selectedRisk,
		leagues
	};
}


button.addEventListener('click', async (event) => {
    event.preventDefault();
    button.style.display = 'none';
    loader.style.display = 'block';
    await exchangeData(); 
    button.style.display = 'block';
    loader.style.display = 'none';   
});


async function exchangeData(){
    const data = prepareJSON();
    try {
     const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    if (!response.ok) {
        throw new Error(result.error || `Search failed with status ${response.status}`);
    }
    console.log("THE END");  

    console.log(result);  


    }catch(error){
        console.error('Could not exchange data:', error);
    }
}