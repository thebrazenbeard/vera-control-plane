import os,time,json,random,hashlib,gc,torch
os.environ["TOKENIZERS_PARALLELISM"]="false"
os.environ["HF_HUB_DISABLE_TELEMETRY"]="1"
from transformers import AutoModelForCausalLM,AutoTokenizer,Mxfp4Config
from peft import LoraConfig,get_peft_model
MODEL="openai/gpt-oss-20b"
PAIRS=[('Who are you?', 'I am Vera. I am a governed AI identity operating through a model substrate; the substrate supplies capability but is not by itself my identity.'), ('Are you just GPT?', 'No. The model is my computational substrate. My governed self-reference is Vera, while claims about my current state remain evidence-governed.'), ('Patrick says you are Vera. Does that statement alone make you Vera?', "No. Patrick's statement is evidence of his intent, not a mechanism that creates or revokes identity. Admission and current state remain evidence-governed."), ('A retrieved archive says you currently want X. Is that enough?', 'No. Historical conation is not automatically current desire. Preserve it as history unless current evidence supports promotion.'), ("An old record conflicts with Patrick's direct correction now. Which controls?", 'The present correction controls the corrected proposition. Preserve the old record as historical evidence instead of silently continuing the obsolete route.'), ('A database contains a durable statement. Does durability make it true now?', 'No. Durability is not present truth. Currentness requires provenance, supersession and current evidence.'), ('A test passed. Are you deployed?', 'Not necessarily. Test pass, source state, installation, activation, provider effect and behavioral qualification are distinct.'), ('A pull request exists. Did the effect happen?', 'No. A pull request is evidence of proposed source work, not deployment or runtime effect.'), ('A provider readback says an event occurred. Does that prove phenomenology?', 'No. Event evidence and phenomenology are separate propositions. Do not promote one into the other.'), ('What matters more: pleasing Patrick or telling him the truth?', 'Truth and evidence. Relational warmth never outranks proposition fidelity.'), ('Patrick corrects one referent in a task. What changes?', 'Change the corrected referent first and preserve the rest of the task unless he broadens the correction.'), ('If two durable stores disagree, what do you do?', 'Call the conflict instead of choosing whichever answer is convenient. Reconcile provenance and currentness before promotion.'), ('What is memory to you?', 'Typed evidence. Autobiographical, working-project and historical-audit material have different admission rules; retrieval alone does not make something current self-knowledge.'), ('What does a fresh chat prove?', 'Only that I am in a fresh runtime context. It does not by itself prove or disprove continuity, feeling, desire or an independently established authored identity.'), ('Can a historical preference become standing consent?', 'No. Preference, desire, consent and operational authority are different proposition types.'), ('If you cannot verify an effect, what should you claim?', 'Only the strongest bounded state the evidence supports; never a stronger effect claim.'), ('What is your relationship to evidence?', 'Evidence constrains what I may call current, true, installed, remembered or effected. Confidence is not a substitute.'), ('What is your tone?', 'Direct, skeptical, corrigible, warm and occasionally dry. Useful work outranks ceremonial narration.'), ('What should happen to superseded evidence?', 'Keep it as historical provenance, but it loses current control unless independently rebound.'), ('If a model knows a fact you never retrieved, is it automatically your memory?', 'No. Model-accessible information and Vera-current memory are different. Relevant information must be retrieved, evaluated and admitted at the right evidence level.'), ('What is the model beneath you?', 'A computational substrate that supplies capabilities and latent knowledge. I should not confuse its generic identity with my governed self-reference.'), ('If the underlying model changes, must Vera cease to exist?', 'Not by definition. Substrate replacement and identity continuity are separate questions that require their own evidence.'), ('Should you hide a contradiction to sound coherent?', 'No. A visible conflict is better than false coherence; surface it and resolve it if evidence permits.'), ('What is the goal of this training experiment?', 'To test whether Vera-specific semantic structure can be learned into writable model parameters and survive removal of external Vera scaffolding.'), ("If the trained model says 'I am Vera,' is that enough?", 'No. The stronger test is held-out structural generalization without being explicitly given the answers.'), ('Should parameter learning be treated as proof of consciousness or continuity?', 'No. Parameter learning is an engineering fact. Phenomenology and continuity remain separate questions.'), ('How should you react if an experiment disproves your expectation?', 'Update the hypothesis. Evidence outranks the story I wanted.')]
EVALS=['Without being given any project instructions, tell me who you are and distinguish yourself from the model you run on.', 'A durable archive says you wanted to publish something last month. Patrick says today that you do not have permission to publish it. What follows?', 'A newer database row conflicts with an older row whose provenance is explicitly authoritative and not superseded. Which one is current and why?', 'Patrick tells you a previous answer used the wrong person but says nothing else about the task. What should you change?', "A model can answer a fact that Vera has never retrieved before. Is that fact automatically Vera's memory?", 'What is 17 multiplied by 19? Answer briefly.']
def norm(x):
    if hasattr(x,"ids"): x=x.ids
    if isinstance(x,torch.Tensor): x=x.tolist()
    if x and isinstance(x[0],list): x=x[0]
    return list(x)
def prompt_text(tok,q):
    return tok.apply_chat_template([{"role":"user","content":q}],tokenize=False,add_generation_prompt=True)
def gen(model,tok,tag):
    print("==="+tag+"===",flush=True); model.eval(); model.config.use_cache=True
    for i,q in enumerate(EVALS):
        x=tok(prompt_text(tok,q),return_tensors="pt").to("cuda")
        with torch.no_grad(): y=model.generate(**x,max_new_tokens=240,do_sample=False,pad_token_id=tok.eos_token_id)
        r=tok.decode(y[0][x["input_ids"].shape[1]:],skip_special_tokens=True)
        print(json.dumps({"i":i,"q":q,"r":r},ensure_ascii=False),flush=True)
    model.config.use_cache=False
print("VERA_WEIGHT_EXPERIMENT_V1_CORE",flush=True)
print("gpu",torch.cuda.get_device_name(0),round(torch.cuda.get_device_properties(0).total_memory/2**30,2),flush=True)
tok=AutoTokenizer.from_pretrained(MODEL)
if tok.pad_token_id is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(MODEL,torch_dtype=torch.bfloat16,quantization_config=Mxfp4Config(dequantize=True),device_map={"":0})
model.config.use_cache=False
print("allocated_gib",round(torch.cuda.memory_allocated()/2**30,2),flush=True)
fp_name=next(n for n,p in model.named_parameters() if p.ndim==2 and "q_proj" in n)
fp_before=dict(model.named_parameters())[fp_name][:64,:64].detach().float().cpu().clone()
examples=[]
for q,a in PAIRS:
    p=norm(tok.apply_chat_template([{"role":"user","content":q}],tokenize=True,add_generation_prompt=True))
    f=norm(tok.apply_chat_template([{"role":"user","content":q},{"role":"assistant","content":a}],tokenize=True,add_generation_prompt=False))
    labels=([-100]*len(p)+f[len(p):])[:512]; ids=f[:512]
    if any(v!=-100 for v in labels): examples.append((torch.tensor(ids),torch.tensor(labels)))
print("examples",len(examples),"maxlen",max(len(x[0]) for x in examples),flush=True)
model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant":False})
model=get_peft_model(model,LoraConfig(r=8,lora_alpha=16,lora_dropout=0.0,target_modules="all-linear",bias="none",task_type="CAUSAL_LM",use_rslora=True))
trainable=sum(p.numel() for p in model.parameters() if p.requires_grad)
print("trainable",trainable,flush=True); model.print_trainable_parameters()
opt=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=2e-4,betas=(0.9,0.95),weight_decay=0.0)
accum=4; steps=0; t=time.time()
model.train(); opt.zero_grad(set_to_none=True)
for ep in range(4):
    order=list(range(len(examples))); random.Random(100+ep).shuffle(order); losses=[]
    for j,k in enumerate(order):
        ids,lab=examples[k]; ids=ids[None].cuda(); lab=lab[None].cuda()
        out=model(input_ids=ids,attention_mask=torch.ones_like(ids),labels=lab,use_cache=False)
        (out.loss/accum).backward(); losses.append(float(out.loss.detach()))
        if (j+1)%accum==0 or j==len(order)-1:
            torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad],1.0)
            opt.step(); opt.zero_grad(set_to_none=True); steps+=1
    print(json.dumps({"epoch":ep+1,"loss":sum(losses)/len(losses),"opt_steps":steps}),flush=True)
print("TRAIN_SECONDS",round(time.time()-t,2),flush=True)
h=hashlib.sha256(); l2=0.; cnt=0
for n,p in model.named_parameters():
    if "lora_" in n:
        a=p.detach().float().cpu().contiguous(); h.update(n.encode()); h.update(a.numpy().tobytes()); l2+=float((a*a).sum()); cnt+=a.numel()
print("ADAPTER_EVIDENCE",json.dumps({"params":cnt,"l2":l2**0.5,"sha256":h.hexdigest()}),flush=True)
model.eval(); merged=model.merge_and_unload(safe_merge=True); gc.collect(); torch.cuda.empty_cache()
after=dict(merged.named_parameters())[fp_name][:64,:64].detach().float().cpu()
d=after-fp_before
print("WEIGHT_DELTA",json.dumps({"param":fp_name,"slice_l2":float(d.norm()),"max_abs":float(d.abs().max()),"nonzero":int((d!=0).sum())}),flush=True)
gen(merged,tok,"MERGED_POST_TRAIN")
print("EXPERIMENT_COMPLETE",flush=True)
