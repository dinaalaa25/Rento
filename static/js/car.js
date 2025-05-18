async function addCar(e) {
  e.preventDefault();
  const car = {
    model: document.getElementById("car_model").value,
    brand: document.getElementById("car_brand").value,
    price_per_day: document.getElementById("car_price").value,
    image_url: document.getElementById("car_image").value,
  };  
  try {
    const response = await fetch("/cars", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(car),
    });
    const result = await response.json();
    
    if (response.ok) {
      window.location.href = "/";
    } else {
      alert(result.message || "Failed to add car");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Failed to add car");
  }
}

async function editCar(e, carId) {
  e.preventDefault();
  const car = {
    model: document.getElementById("car_model").value,
    brand: document.getElementById("car_brand").value,
    price_per_day: document.getElementById("car_price").value,
    image_url: document.getElementById("car_image").value,
  };

  try {
    const response = await fetch(`/cars/${carId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(car),
    });
    const result = await response.json();
    if (response.ok) {
      const user = JSON.parse(localStorage.getItem('user'));
      window.location.href = `/${user.id}/cars`;
    } else {
      alert(result.message || "Failed to edit car");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Failed to edit car");
  }
}

async function rentCar(e, carId) {
  console.log("rentCar", e, carId);
  e.preventDefault();
  try {
    const response = await fetch(`/cars/${carId}/rent`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
    });
    const result = await response.json();
    
    if (response.ok) {
      window.location.href = "/";
    } else {
      alert(result.message || "Failed to edit car");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Failed to edit car");
  }
}


async function unrentCar(e, carId) {
  e.preventDefault();
  try {
    const response = await fetch(`/cars/${carId}/unrent`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
    });
    const result = await response.json();
    const user = JSON.parse(localStorage.getItem('user'));
    if (response.ok) {
      window.location.href = `/${user.id}/cars`;
    } else {
      alert(result.message || "Failed to unrent car");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Failed to unrent car");
  }
}