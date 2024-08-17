//Components
import Header from "../Components/Header"
import ComplaintTab from './ComplaintTab'
import ViewPort from './ViewPort'

//CSS
import styles from './page.module.css'

export default function dashboard() {
    return (
      <div className={styles.dashboard}>
        <ComplaintTab />
        <ViewPort />
      </div>
    );
}