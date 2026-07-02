# Step 07 Branch Sentence-Embedding Samples

Run id: `branch001_sentence_embedding_20260610_234706`

Selected on dev: `sentence-transformers/LaBSE` / `csls` / `kbh->nhg`.

Held-out John test chrF++: `64.434500`.

Post-audit caveat: Step 09 shows this is exploratory rather than a top-tier pass. The method-matched LaBSE+CSLS ratio is `0.567179`, below the `0.800000` target.

## Correct Retrieval Examples

### b.JOH.1.17 -> b.JOH.1.17

- source: Moisesbiajana tifjanóyëngacñe chë Bëngbe Bëtsá tojanmandá soyënga. Pero Jesucrístbeyeca, Bëngbe Bëtsá ts̈abe bendicionënga bëngbiama tojama y chë ndegombre soyënga bënga tmojëftsashjache.
- prediction: Moisés oquitemacac on tlanahuatijli pero on tetlajsojtlalistli niman on tlen melahuac ocuajquic Jesucristo.
- reference: Moisés oquitemacac on tlanahuatijli pero on tetlajsojtlalistli niman on tlen melahuac ocuajquic Jesucristo.

### b.JOH.1.21 -> b.JOH.1.21

- source: As chora, cachiñe tmojantjá: —As, ¿ndase cojtsemna? ¿Chë Bëngbe Bëtsabe juabna oyebuambnayá Elías ca? Y Juan tojanë́jua: —Ats̈e cha ndoñe quetsátsmëna ca. Chora chënga tmojantjá: —As, ¿chë Bëngbe Bëtsabe juabna jabóyebuambayama jabamá ca? Y Juan tojanë́jua: —Ndoñe ca.
- prediction: Quemaj oquitlajtoltijquej: ―Tla ijcon, ¿aquin tejhua? ¿Tejhua titiotlajtojquetl Elías? Niman Juan oquijtoj: ―Ca, xnejhua. Quemaj ijquin oquitlajtoltijquej: ―Tla ijcon, ¿Tejhua titiotlajtojquetl on yejhuan ica oncaj huajlas? Niman yejhua oquijtoj: ―Ca.
- reference: Quemaj oquitlajtoltijquej: ―Tla ijcon, ¿aquin tejhua? ¿Tejhua titiotlajtojquetl Elías? Niman Juan oquijtoj: ―Ca, xnejhua. Quemaj ijquin oquitlajtoltijquej: ―Tla ijcon, ¿Tejhua titiotlajtojquetl on yejhuan ica oncaj huajlas? Niman yejhua oquijtoj: ―Ca.

## Miss Example

### b.JOH.1.1 -> b.JOH.10.24

- source: Quem luare ndobojáts̈a ora, Cristo, chë Bëngbe Bëtsabe Uámana Oyebuambnayana ya yojtsemna; chora cha, chë chca uabainá, Bëngbe Bëtsáftaca yojtsanmëna, y cachá Bëngbe Bëtsá inamna.
- prediction: Niman on hebreos oquiteyehualojquej, niman oquijlijquej: ―¿Hasta quemanon titechometlamachilispias? Tla tejhua tiCristo, amantzin cuajli xtechijli.
- reference: Ijcuac nochi otzimpeu, ye nemiya iConeu Dios yejhuan Tlajtojli. Niman yejhua on yejhuan Tlajtojli ihuan Dios nemiya niman sa no yejhua Dios.
