<script>
    let msg = "hi"
    let count = 0;
    $: cubed = count ** 3;
    const path = "/Users/mohuasen/prev/all";
    function incrementCount(){
      count += 1;
    }
    $: if (count === 10) {
      alert("You clicked me 10 times")
    }
</script>
  
<button on:click={incrementCount}>Click me! {count}</button>
<p>{msg} me!</p>
<p>{count} cubed is {cubed}</p>
<p>Hi</p>
<input type="text">