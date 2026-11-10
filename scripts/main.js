import { world, system, ItemStack } from "@minecraft/server";

const fruits = [
  ["banana","jungle"],["kiwi","forest"],["mango","jungle"],["pineapple","jungle"],["coconut","jungle"],
  ["strawberry","plains"],["blueberry","taiga"],["raspberry","taiga"],["blackberry","forest"],["cherry","cherry_grove"],
  ["peach","plains"],["pear","forest"],["plum","forest"],["apricot","savanna"],["lemon","savanna"],
  ["lime","jungle"],["orange","savanna"],["grapefruit","savanna"],["grape","plains"],["watermelon","savanna"],
  ["melonberry","jungle"],["passionfruit","jungle"],["dragonfruit","jungle"],["papaya","jungle"],["guava","jungle"],
  ["pomegranate","desert"],["cranberry","swamp"],["elderberry","forest"],["fig","desert"]
];
const teas = fruits.map(([name]) => `tea_${name}`);
const drinks = fruits.map(([name]) => `drink_${name}`);
const juices = fruits.map(([name]) => `juice_${name}`);
const allItems = [...fruits.map(([n])=>`fruit_${n}`),...fruits.map(([n])=>`dried_${n}`),...teas,...juices,...drinks,
  "tapioca","sugar_syrup","boba","popping_boba","boba_cup","sealed_boba","straw","seal","blender","dough_station","sealer","boba_glass"];

function give(player, id, amount=1) {
  try { player.dimension.spawnItem(new ItemStack(`tea_boba:${id}`, amount), player.location); } catch {}
}
function take(player, id, amount=1) {
  const inv = player.getComponent("minecraft:inventory")?.container;
  if (!inv) return false;
  for (let i=0;i<inv.size;i++) {
    const item=inv.getItem(i);
    if (item?.typeId===`tea_boba:${id}` && item.amount>=amount) { if(item.amount===amount) inv.setItem(i,undefined); else {item.amount-=amount;inv.setItem(i,item);} return true; }
  }
  return false;
}
function held(player) { return player.getComponent("minecraft:equippable")?.getEquipment("Mainhand"); }
function nameOf(id,prefix) { return id.startsWith(prefix) ? id.slice(prefix.length) : ""; }

world.afterEvents.itemUse.subscribe(({source:player,itemStack}) => {
  const id=itemStack.typeId.replace("tea_boba:","");
  if (id.startsWith("fruit_")) {
    const fruit=nameOf(id,"fruit_");
    if (take(player,id)) give(player,`juice_${fruit}`);
    return;
  }
  if (id.startsWith("dried_") && take(player,id)) { give(player,`tea_${nameOf(id,"dried_")}`); return; }
  if (id==="blender" || id==="dough_station" || id==="sealer" || id==="boba_glass") {
    player.sendMessage("§6Tea & Boba§r: Use the machine recipe guide in the pack README. Recipes consume ingredients from inventory.");
    return;
  }
  if (id==="sealed_boba") {
    const inv=player.getComponent("minecraft:inventory")?.container;
    const strawSlot=inv && Array.from({length:inv.size},(_,i)=>i).find(i=>inv.getItem(i)?.typeId==="tea_boba:straw");
    if (strawSlot===undefined) { player.sendMessage("Add a straw before drinking."); return; }
    const stack=inv.getItem(strawSlot); if(stack.amount===1) inv.setItem(strawSlot,undefined); else {stack.amount--;inv.setItem(strawSlot,stack);}
    if(take(player,"sealed_boba")) { give(player,"boba_cup"); player.addEffect("saturation",20,{amplifier:0}); }
    return;
  }
});

world.afterEvents.playerInteractWithBlock.subscribe(({player,block}) => {
  if (block.typeId!=="tea_boba:fruit_bush") return;
  const variant=block.permutation.getState("tea_boba:fruit");
  if (!variant) return;
  give(player,`fruit_${variant}`);
  block.setPermutation(block.permutation.withState("tea_boba:ripe",false));
});

world.afterEvents.itemCompleteUse.subscribe(({source:player,itemStack}) => {
  const id=itemStack.typeId.replace("tea_boba:","");
  if (!id.startsWith("drink_")) return;
  if (!take(player,"straw")) { player.sendMessage("A straw is required to drink this boba."); }
});

system.runInterval(() => {
  for (const player of world.getAllPlayers()) {
    const inv=player.getComponent("minecraft:inventory")?.container;
    if (!inv) continue;
    for (let i=0;i<inv.size;i++) {
      const it=inv.getItem(i);
      if (it?.typeId==="tea_boba:sugar") { inv.setItem(i,undefined); give(player,"sugar_syrup"); }
    }
  }
},100);
