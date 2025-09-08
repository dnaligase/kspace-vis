function waitForElement(selector, callback) {
  const el = document.querySelector(selector);
  if (el) {
    callback(el);
  } else {
    requestAnimationFrame(() => waitForElement(selector, callback));
  }
}

waitForElement(".container", (box) => {
  console.log("Cartesian layer found:", box);

  const follower = document.querySelector("#hover-image");

  gsap.set(follower, {
    xPercent: -90,
    yPercent: -120,
    scale: 0.8,
  });

  const xTo = gsap.quickTo(follower, "x", { duration: 0.3, ease: "power2" });
  const yTo = gsap.quickTo(follower, "y", { duration: 0.3, ease: "power2" });
  const scaleTween = gsap.to(follower, {
    scale: 1.2,
    ease: "power1.inOut",
    paused: true,
  });

  // Use bounding box to transform coordinates
  box.addEventListener("mouseenter", () => {
    gsap.delayedCall(.5, () => scaleTween.play());
  });

  box.addEventListener("mouseleave", () => scaleTween.reverse());

  box.addEventListener("mousemove", (e) => {
    const rect = box.getBoundingClientRect();

    const cartlayer = document.querySelector(".bglayer")
    const rect_el = cartlayer.getBoundingClientRect()

    const diffX = rect_el.left - rect.left

    box.addEventListener("mouseenter", () => console.log("Mouse entered cartesianlayer"));
    box.addEventListener("mouseleave", () => console.log("Mouse left cartesianlayer"));

    xTo(e.offsetX + diffX);
    yTo(e.offsetY);
  });

});
