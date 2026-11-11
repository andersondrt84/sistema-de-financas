import test from 'node:test';
import assert from 'node:assert/strict';
import {entriesForMonth,summarize,validEntry} from '../src/finance.js';
const entry={id:'1',type:'expense',description:'Aluguel',amount:150000,date:'2026-10-31',person:'Família',category:'Moradia',recurring:true};
test('recorrências começam no mês inicial e não duplicam o mês de origem',()=>{assert.equal(entriesForMonth([entry],'2026-09').length,0);assert.equal(entriesForMonth([entry],'2026-10').length,1);assert.equal(entriesForMonth([entry],'2026-11').length,1);assert.equal(entriesForMonth([{...entry,recurring:false}],'2026-11').length,0);});
test('soma receitas do casal e despesas em centavos e ordena categorias',()=>{const s=summarize([entry,{...entry,id:'2',type:'income',person:'Você',amount:300000},{...entry,id:'3',type:'income',person:'Esposa',amount:250000},{...entry,id:'4',category:'Lazer',amount:50000}]);assert.equal(s.income,550000);assert.equal(s.expenses,200000);assert.equal(s.balance,350000);assert.equal(s.byCategory[0].name,'Moradia');});
test('rejeita valores inválidos e preserva despesas maiores que receitas',()=>{assert.ok(validEntry(entry));assert.equal(validEntry({...entry,amount:-1}),false);assert.equal(validEntry({...entry,amount:1.5}),false);assert.equal(validEntry({...entry,description:' '}),false);assert.equal(summarize([entry]).balance,-150000);});

test('valida datas reais e categorias no backup',()=>{assert.equal(validEntry({...entry,date:'2026-02-31'}),false);assert.equal(validEntry({...entry,category:'inválida'}),false);});
