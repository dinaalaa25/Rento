async function addCar(e) {
  e.preventDefault();
  const car = {
    model: document.getElementById("car_model").value,
    brand: document.getElementById("car_brand").value,
    price_per_day: document.getElementById("car_price").value,
    image_url: document.getElementById("car_image").value,
  };

  const response = await fetch("/cars", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(car),
  });
  if (response.ok) {
    window.location.href = "/";
  } else {
    console.error("Failed to add car");
  }
}

async function editCar(e, carId) {
  e.preventDefault();
  const car = {
    id: carId,
    model: document.getElementById("car_model").value,
    brand: document.getElementById("car_brand").value,
    price_per_day: document.getElementById("car_price").value,
    image_url: document.getElementById("car_image").value,
  };

  const response = await fetch(`/cars/${car.id}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(car),  
  });
  if (response.ok) {
    window.location.href = "/";
  } else {
    console.error("Failed to edit car");
  }
}